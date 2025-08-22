from django.contrib import admin
from .models import Event, ArduinoSchedule

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("id", "sensor", "message", "created_at")
    list_filter = ("sensor", "message", "created_at")
    search_fields = ("sensor", "message")
    ordering = ("-created_at",)


@admin.register(ArduinoSchedule)
class ArduinoScheduleAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "start_time", "end_time", "created_at", "updated_at")
    list_filter = ("user", "start_time", "end_time", "created_at", "updated_at")
    search_fields = ("user", "start_time", "end_time")
    ordering = ("-created_at",)