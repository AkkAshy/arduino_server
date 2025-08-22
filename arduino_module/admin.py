from django.contrib import admin
from .models import ArduinoDevice

@admin.register(ArduinoDevice)
class ArduinoDeviceAdmin(admin.ModelAdmin):
    list_display = ('login', 'registered_at')
    search_fields = ('login', 'registered_at')
    list_filter = ('login',)