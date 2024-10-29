from rest_framework import serializers
from .models import Assignment, Admin
from django.contrib.auth.models import User

# Serializer for Assignment model
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['task', 'file', 'admin']

# Serializer for Admin model
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Admin

class AdminSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  # Get username from related User

    class Meta:
        model = Admin
        fields = ['id', 'username', 'department']  # Include username and department
        read_only_fields = ['id']  # Optional: Make 'id' read-only if you don't want to modify it

      
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user