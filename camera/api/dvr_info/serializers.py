from rest_framework import serializers
from ...models import DvrInfo


class DvrInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DvrInfo
        fields = '__all__'
