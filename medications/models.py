from django.db import models

class Medication(models.Model):
    name = models.CharField(max_length=150)
    dosage = models.IntegerField()
    unity = models.CharField(max_length=50)
    manufacturer = models.TextField()
    composition = models.TextField()
    therapeutic_class = models.TextField()
    atc = models.CharField(max_length=20)
    public_price = models.DecimalField(max_digits=10, decimal_places=2)
    hospital_price = models.DecimalField(max_digits=10, decimal_places=2)
    indications = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} {self.dosage}{self.unity}"
