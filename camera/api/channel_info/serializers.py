from rest_framework import serializers
from ...models import ChannelInfo


class ChannelInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChannelInfo
        fields = '__all__'
