from django.db import models

class Medication(models.Model):
    name = models.CharField(max_length=200)
    presentation = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    distributor = models.CharField(max_length=100)
    composition = models.TextField(blank=True)
    family = models.CharField(max_length=100)
    status = models.CharField(max_length=50)
    atc_code = models.CharField(max_length=15)
    public_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default=None
    )
    hospital_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        default=None
    )
    table = models.CharField(max_length=1)
    indication = models.TextField()
    
    def __str__(self):
        return f"{self.name} ({self.dosage})"