from rest_framework import serializers


class ResourceStatisticSerializer(serializers.Serializer):
    year = serializers.CharField()
    name = serializers.CharField()
    count = serializers.IntegerField()
