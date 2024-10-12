from rest_framework import serializers
from .models import Assignment, Admin
from django.contrib.auth.models import User

# Serializer for Assignment model
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['task', 'file', 'admin']

# Serializer for Admin model
class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['id', 'username', 'password','department']
        extra_kwargs = {'password': {'write_only': True}}

      
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user