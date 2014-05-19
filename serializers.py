from rest_framework import serializers

from models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource


class ResourceStatisticSerializer(serializers.Serializer):
    year = serializers.CharField()
    name = serializers.CharField()
    count = serializers.IntegerField()
    total_price = serializers.DecimalField(decimal_places=2)
