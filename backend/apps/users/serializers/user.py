from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user list and detail views"""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'avatar', 
            'city', 'country', 'date_of_birth', 'is_active', 
            'created_at', 'updated_at', 'last_login'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'last_login']

class UserUpdateSerializer(serializers.ModelSerializer):
    """Serializer for user update"""
    
    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'avatar', 
            'city', 'country', 'date_of_birth'
        ]

class UserOwnSerializer(serializers.ModelSerializer):
    """Serializer for user's own profile"""
    
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'avatar', 
            'city', 'country', 'date_of_birth', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'email', 'created_at', 'updated_at']