from django.urls import path
from .views import ArduinoRegisterView

urlpatterns = [
    path('arduino/register/', ArduinoRegisterView.as_view(), name='arduino-register'),
]
