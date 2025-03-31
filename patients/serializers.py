from rest_framework import serializers
from physicians.models import Physician
from .models import Patient

class PatientSerializer(serializers.ModelSerializer):
    physician_id = serializers.PrimaryKeyRelatedField(
        queryset=Physician.objects.all(),
        many=True,
        required=False
    )
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'physician_id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'birthday',
            'gender',
            'weight',
        ]

    def validate_phone(self, value):
        if len(str(value)) != 10:
            raise serializers.ValidationError("Phone number must be 10 digits long")
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must be a number")
        return value

    def validate_weight(self, value):
        if value <= 0:
            raise serializers.ValidationError("Weight must be a positive number")
        return value
    
    def validate_email(self, value):
        if Patient.objects.filter(email=value).exists():
            raise serializers.ValidationError("A patient with this email already exists.")
        return value