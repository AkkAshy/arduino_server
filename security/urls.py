from django.urls import path
from .views import receive_event, list_events, ArduinoScheduleView

urlpatterns = [
    path("event/", receive_event, name="receive_event"),
    path("events/", list_events, name="list_events"),
    path("schedule/", ArduinoScheduleView.as_view(), name="schedule"),
]
