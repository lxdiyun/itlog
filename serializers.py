from rest_framework import serializers

from models import Resource


class ResourceSerializer(serializers.ModelSerializer):
    recent_logs = serializers.SerializerMethodField('get_recent_logs')

    class Meta:
        model = Resource

    def get_recent_logs(self, obj):
        return obj.get_recent_logs()


class ResourceStatisticSerializer(serializers.Serializer):
    year = serializers.CharField()
    name = serializers.CharField()
    count = serializers.IntegerField()
    total_price = serializers.DecimalField(decimal_places=2)
