from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Event, ArduinoSchedule
from .serializers import EventSerializer, ArduinoScheduleSerializer
from arduino_module.models import ArduinoDevice

@api_view(["POST"])
def receive_event(request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
        event = serializer.save()

        # 🚨 здесь можно отправить уведомление
        # send_sms(event.message)
        # send_telegram(event.message)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
def list_events(request):
    events = Event.objects.all().order_by("-created_at")[:50]  # последние 50
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)




class ArduinoScheduleView(APIView):
    def post(self, request):
        login = request.data.get("login")
        password = request.data.get("password")

        if not login or not password:
            return Response({"error": "Не указан логин или пароль"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = ArduinoDevice.objects.get(login=login)
        except ArduinoDevice.DoesNotExist:
            return Response({"error": "Неверный логин"}, status=status.HTTP_401_UNAUTHORIZED)

        # Если храним plain текст
        if user.password != password:
            return Response({"error": "Неверный пароль"}, status=status.HTTP_401_UNAUTHORIZED)

        # Если используем хеши, то:
        # if not check_password(password, device.password):
        #     return Response({"error": "Неверный пароль"}, status=status.HTTP_401_UNAUTHORIZED)

        # Обновляем или создаем расписание
        serializer = ArduinoScheduleSerializer(data=request.data)
        if serializer.is_valid():
            schedule, created = ArduinoSchedule.objects.update_or_create(
                user=user,
                defaults=serializer.validated_data
            )
            return Response({"message": "Расписание обновлено"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
