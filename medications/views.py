from django.views.generic import ListView, DetailView
from rest_framework import generics
from django.db.models import Q

from .serializers import MedicationSerializer
from .models import Medication

class MedicationListView(generics.ListAPIView):
    serializer_class = MedicationSerializer
    queryset = Medication.objects.all()
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search')
        if search:
            return queryset.filter(
                Q(name__icontains=query) |
                Q(dosage__icontains=query) |
                Q(atc_code__icontains=query)
            )
        return queryset

class MedicationDetailView(generics.RetrieveAPIView):
    queryset = Medication.objects.all()
    serializer_class = MedicationSerializer
    context_object_name = 'medication'

class MedicationTemplateView(ListView):
    model = Medication
    template_name = 'medications/list.html'
    context_object_name = 'medications'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(composition__icontains=search_query) |
                Q(atc_code__icontains=search_query)
            )
        return queryset.order_by('name')

class MedicationTemplateDetailView(DetailView):
    queryset = Medication.objects.all()
    template_name = 'medications/detail.html'
    context_object_name = 'medication'