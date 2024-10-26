from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from django.conf import settings
from authlib.integrations.django_client import OAuth
from .models import CoolgoatUser
from .serializers import CoolgoatUserSerializer
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from urllib.parse import urlencode
            
class UserCreateView(APIView):
    def post(self, request):
        serializer = CoolgoatUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'success', 'email': user.email}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserGetView(APIView):
    def get(self, request, user_email):
        user = CoolgoatUser.objects.get(email=user_email)
        serializer = CoolgoatUserSerializer(user)
        return Response({'status': 'success', 'user': serializer.data}, status=status.HTTP_200_OK)


class WalletUpdateView(APIView):
    renderer_classes = [JSONRenderer]
    def post(self, request, user_email):
        try:
            value = request.data.get("value")
            if not value or int(value) <= 0:
                return Response({"error": "Invalid value"}, status=status.HTTP_400_BAD_REQUEST)
            user = CoolgoatUser.objects.get(email=user_email)
            user.funds += int(value)
            user.save()
            return Response({"balance": user.funds}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)