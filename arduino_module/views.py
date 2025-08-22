from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ArduinoDevice
from .serializer import ArduinoDeviceSerializer
from django.contrib.auth.models import User

class ArduinoRegisterView(APIView):

    def post(self, request):
        login = request.data.get('login')
        password = request.data.get('password')

        if not login or not password:
            return Response({'status': 'error', 'message': 'Логин и пароль обязательны'}, status=status.HTTP_400_BAD_REQUEST)

        # Проверяем существует ли Arduino
        try:
            device = ArduinoDevice.objects.get(login=login)
            # Проверка пароля
            if device.password == password:
                return Response({'status': 'success', 'message': 'Arduino авторизована'})
            else:
                return Response({'status': 'error', 'message': 'Неверный пароль'}, status=status.HTTP_401_UNAUTHORIZED)
        except ArduinoDevice.DoesNotExist:
            # Создаём нового пользователя и устройство
            user, created = User.objects.get_or_create(username=login)
            device = ArduinoDevice.objects.create(owner=user, login=login, password=password)
            return Response({'status': 'success', 'message': 'Arduino зарегистрирована'})


class ArduinoProfileUpdateView(APIView):
    def post(self, request, login):
        try:
            device = ArduinoDevice.objects.get(login=login)
        except ArduinoDevice.DoesNotExist:
            return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ArduinoDeviceSerializer(device, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Данные обновлены"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)