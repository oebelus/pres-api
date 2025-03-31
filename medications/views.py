from django.views.generic import ListView, DetailView
from rest_framework import generics
from django.db.models import Q

from .serializers import MedicationSerializer
from .models import Medication

class MedicationListView(generics.ListAPIView):
    serializer_class = MedicationSerializer

    def get_queryset(self):
        queryset = Medication.objects.all()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(composition__icontains=search_query) |
                Q(therapeutic_class__icontains=search_query) |
                Q(atc__icontains=search_query)
            )
        return queryset.order_by('name')
    
class MedicationTemplateView(ListView):
    model = Medication
    template_name = 'medications/list.html'
    context_object_name = 'medications'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query) |
                Q(composition__icontains=search_query) |
                Q(therapeutic_class__icontains=search_query) |
                Q(atc__icontains=search_query)
            )
        return queryset.order_by('name')