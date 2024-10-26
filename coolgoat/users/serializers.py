from rest_framework import serializers
from .models import CoolgoatUser

class CoolgoatUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoolgoatUser
        fields = ['email', 'funds']
