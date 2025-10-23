from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError("User don't have account")
            if not user.is_active:
                raise serializers.ValidationError("Your account is disable")
            attrs['user'] = user 
            return attrs
        else:
            raise serializers.ValidationError("Must include email and password")
        
class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
    def validate(self, attrs):
        refresh = attrs.get('refresh')
        if not refresh:
            raise serializers.ValidationError("Refresh token is required")
        return attrs
