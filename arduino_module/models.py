from django.db import models
from django.contrib.auth.models import User
import uuid

class ArduinoDevice(models.Model):
    login = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Можно хранить хеш
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.login
    def set_password(self, password):
        self.password = password



    class Meta:
        verbose_name = "Ардуино"
        verbose_name_plural = "Ардуины"