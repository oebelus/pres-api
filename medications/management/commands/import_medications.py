import json
from django.core.management.base import BaseCommand
from medications.models import Medication

class Command(BaseCommand):
    help = 'Imports medications from JSON file'

    def handle(self, *args, **options):
        try:
            with open('medications.json', 'r', encoding='utf-8') as f:
                medications = json.load(f)
                
                for med in medications:
                    try:
                        public_price = float(med['ppv']) if med.get('ppv') is not None else None
                    except (TypeError, ValueError):
                        public_price = None
                        self.stdout.write(self.style.WARNING(f"Invalid public price for {med['name']}"))
                    
                    try:
                        hospital_price = float(med['prix_hospitalier']) if med.get('prix_hospitalier') is not None else None
                    except (TypeError, ValueError):
                        hospital_price = None
                        self.stdout.write(self.style.WARNING(f"Invalid hospital price for {med['name']}"))
                    
                    Medication.objects.create(
                        name=med['name'],
                        presentation=med.get('presentation', ''),
                        dosage=med.get('dosage', ''),
                        distributor=med.get('distributeur', ''),
                        composition=med.get('composition', ''),
                        family=med.get('famille', ''),
                        status=med.get('statut', ''),
                        atc_code=med.get('atc', ''),
                        public_price=public_price,
                        hospital_price=hospital_price,
                        table=med.get('tableau', ''),
                        indication=med.get('indication', '')
                    )
                
                self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(medications)} medications'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))