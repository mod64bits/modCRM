from rest_framework import serializers
from .models import RondaPoint, RondaLog

class RondaPointSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.name', read_only=True)

    class Meta:
        model = RondaPoint
        fields = ['id', 'name', 'location_description', 'company', 'company_name', 'created_at']
        read_only_fields = ['id', 'company_name', 'created_at']


class RondaLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    ronda_point_name = serializers.CharField(source='ronda_point.name', read_only=True)
    location_description = serializers.CharField(source='ronda_point.location_description', read_only=True)

    class Meta:
        model = RondaLog
        fields = ['id', 'ronda_point', 'user', 'user_name', 'ronda_point_name', 'location_description', 'timestamp']
        read_only_fields = ['id', 'user', 'user_name', 'ronda_point_name', 'location_description', 'timestamp']


