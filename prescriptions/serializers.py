from rest_framework import serializers
from .models import Prescription, PrescriptionMedication

class PrescriptionMedicationSerializer(serializers.ModelSerializer):
    medication_name = serializers.CharField(source='medication.name', read_only=True)
    
    class Meta:
        model = PrescriptionMedication
        fields = [
            'id',
            'medication',
            'medication_name',
            'dosage_instruction',
            'duration_days',
            'refills'
        ]

class PrescriptionSerializer(serializers.ModelSerializer):
    medications = PrescriptionMedicationSerializer(many=True, read_only=True)
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    physician_name = serializers.CharField(source='physician.get_full_name', read_only=True)

    class Meta:
        model = Prescription
        fields = [
            'id',
            'patient',
            'patient_name',
            'physician',
            'physician_name',
            'date',
            'is_active',
            'notes',
            'medications'
        ]
        read_only_fields = ['date']

class CreatePrescriptionSerializer(serializers.ModelSerializer):
    medications = PrescriptionMedicationSerializer(many=True)

    class Meta:
        model = Prescription
        fields = ['patient', 'notes', 'medications']

    def create(self, validated_data):
        medications_data = validated_data.pop('medications')
        prescription = Prescription.objects.create(
            **validated_data,
            physician=self.context['request'].user
        )
        
        for medication_data in medications_data:
            PrescriptionMedication.objects.create(
                prescription=prescription,
                **medication_data
            )
        
        return prescription