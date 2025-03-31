from rest_framework import serializers
from .models import Medication

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = [
            'id',
            'name',
            'dosage',
            'unity',
            'manufacturer',
            'composition',
            'therapeutic_class',
            'atc',
            'public_price',
            'hospital_price',
            'indications',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']