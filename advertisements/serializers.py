from rest_framework import serializers
from advertisements.models import Advertisement, AdvertisementStatusChoices


class AdvertisementSerializer(serializers.ModelSerializer):
    creator = serializers.SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'creator', 'status', 'created_at')

    def validate(self, data):
        if self.instance is None:
            status = data.get('status', AdvertisementStatusChoices.OPEN)
        else:
            status = data.get('status', self.instance.status)

        if status == AdvertisementStatusChoices.OPEN:
            request = self.context['request']
            open_count = Advertisement.objects.filter(
                creator=request.user,
                status=AdvertisementStatusChoices.OPEN,
            ).count()

            if self.instance and self.instance.status == AdvertisementStatusChoices.OPEN:
                open_count -= 1

            if open_count >= 10:
                raise serializers.ValidationError(
                    'У пользователя не может быть больше 10 открытых объявлений'
                )

        return data