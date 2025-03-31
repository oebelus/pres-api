from rest_framework.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView, CreateView
from rest_framework import generics, permissions
from django.urls import reverse_lazy
from .forms import PatientCreateForm

from .models import Patient
from .serializers import PatientSerializer

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only show patients associated th the current physician
        return self.request.user.patients.all()

    def perform_create(self, serializer):
        # Automatically associate the current physician with the new patient
        patient = serializer.save()
        patient.physicians.add(self.request.user)
        patient.save()

class PatientRetrieveView(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        # Only allow access to patients associated with the current physician
        return self.request.user.patients.all()

    def get_object(self):
        patient = super().get_object()
        if not patient.physicians.filter(id=self.request.user.id).exists():
            raise PermissionDenied("You don't have access to this patient")
        return patient
    

class PatientTemplateListView(ListView):
    model = Patient
    template_name = 'patients/list.html'
    context_object_name = 'patients'
    
    def get_queryset(self):
        return self.request.user.patients.all()
    
class PatientTemplateDetailView(DetailView):
    model = Patient
    template_name = 'patients/detail.html'
    context_object_name = 'patient'
    
    def get_queryset(self):
        return self.request.user.patients.all()
    
class PatientCreateView(CreateView):
    form_class = PatientCreateForm
    template_name = 'patients/create.html'
    success_url = reverse_lazy('patient-list')

    def form_valid(self, form):
        # Automatically associate the current physician
        patient = form.save()
        patient.physicians.add(self.request.user)
        return super().form_valid(form)