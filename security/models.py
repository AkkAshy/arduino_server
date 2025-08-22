from django.db import models
from arduino_module.models import ArduinoDevice



class Event(models.Model):
    SENSOR_CHOICES = [
        ("reed", "Геркон"),
        ("pir", "Датчик движения"),
        ("glass", "Датчик разбития стекла"),
    ]
    sensor = models.CharField(max_length=20, choices=SENSOR_CHOICES)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor} - {self.message} ({self.created_at})"

    class Meta:
        verbose_name = "Событие"
        verbose_name_plural = "События"


  # Или ваша кастомная модель Account

class ArduinoSchedule(models.Model):
    user = models.OneToOneField(ArduinoDevice, on_delete=models.CASCADE, related_name='arduino_schedule')
    start_time = models.TimeField(default="00:00")  # Время начала работы
    end_time = models.TimeField(default="23:59")    # Время окончания работы
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Arduino schedule for {self.user}: {self.start_time} - {self.end_time}"
    
    class Meta:
        verbose_name = "Расписание"
        verbose_name_plural = "Расписания"
