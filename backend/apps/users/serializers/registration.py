from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from datetime import date
from apps.users.models import User
from apps.users.utils.generate_otp import is_verified, clear_verification

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        
        email = attrs['email']
        if not is_verified(email, 'register'):
            raise serializers.ValidationError("OTP verification required")
        
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        password = validated_data.pop('password')
        email = validated_data['email']
        
        user = User.objects.create_user(password=password, **validated_data)
        clear_verification(email, 'register')
        return user

class UserProfileCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'city', 'country', 'date_of_birth'
        ]
    
    def validate_first_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("First name is required")
        return value.strip()
    
    def validate_last_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Last name is required")
        return value.strip()
    
    def validate_date_of_birth(self, value):
        if value > date.today():
            raise serializers.ValidationError("Date of birth cannot be in the future")
        return value
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
