from rest_framework import serializers
from .models import PotholeData

class PotholeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PotholeData
        fields = ['id', 'timestamp', 'load_value', 'tilt_status', 'distance', 'label']
