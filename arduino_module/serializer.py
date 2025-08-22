from rest_framework import serializers
from .models import ArduinoDevice

class ArduinoDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArduinoDevice
        fields = ['login', 'password']
