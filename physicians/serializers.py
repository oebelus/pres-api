from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Physician

User = get_user_model()

class PhysicianRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Physician
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'specialty',
            'hospital',
            'university',
            'date_joined',
            'last_login',
        ]
        read_only_fields = ['id', 'date_joined', 'last_login']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_phone(self, value):
        if len(str(value)) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits long")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
    
class PhysicianProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Physician
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'specialty',
            'hospital',
            'university',
            'date_joined',
            'last_login',
        ]
        read_only_fields = ['id', 'email', 'date_joined', 'last_login']

    def validate_phone(self, value):
        if len(str(value)) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits long")
        return value