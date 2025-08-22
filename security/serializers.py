from rest_framework import serializers
from .models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ["id", "sensor", "message", "created_at"]


from rest_framework import serializers
from .models import ArduinoSchedule

class ArduinoScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArduinoSchedule
        fields = ['start_time', 'end_time']
