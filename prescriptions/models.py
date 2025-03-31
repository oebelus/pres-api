from django.db import models

class PrescriptionMedication(models.Model):
    prescription = models.ForeignKey('prescriptions.Prescription', on_delete=models.CASCADE)
    medication = models.ForeignKey('medications.Medication', on_delete=models.CASCADE)
    dosage_instruction = models.TextField()
    duration_days = models.PositiveIntegerField()
    refills = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.medication.name} for {self.prescription}"

class Prescription(models.Model):
    patient = models.ForeignKey('patients.Patient', on_delete=models.CASCADE)
    physician = models.ForeignKey('physicians.Physician', on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Prescription #{self.id} for {self.patient} by {self.physician}"