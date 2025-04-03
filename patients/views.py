from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework import generics, permissions
from django.urls import reverse_lazy
from .forms import PatientCreateForm

from .models import Patient
from .serializers import PatientSerializer

class PatientListCreateView(generics.ListCreateAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    
    def get_queryset(self):
        return self.request.user.patients.all()
    
    def perform_create(self, serializer):
        patient = serializer.save()
        patient.physicians.add(self.request.user)

class PatientRetrieveView(generics.RetrieveAPIView):
    serializer_class = PatientSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    lookup_field = 'id'
    
    def get_queryset(self):
        return self.request.user.patients.all()

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
    

class PatientTemplateListView(LoginRequiredMixin, ListView):
    model = Patient
    template_name = 'patients/list.html'
    context_object_name = 'patients'
    
    def get_queryset(self):
        return self.request.user.patients.all().order_by('last_name')
    
class PatientTemplateDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/detail.html'
    context_object_name = 'patient'
    
    def get_queryset(self):
        return self.request.user.patients.all()

class PatientTemplateDetailView(LoginRequiredMixin, DetailView):
    model = Patient
    template_name = 'patients/detail.html'
    context_object_name = 'patient'
    
    def get_queryset(self):
        return self.request.user.patients.all()

class PatientCreateView(LoginRequiredMixin, CreateView):
    form_class = PatientCreateForm
    template_name = 'patients/create.html'
    success_url = reverse_lazy('patient-list')
    
    def form_valid(self, form):
        patient = form.save()
        patient.physicians.add(self.request.user)
        return super().form_valid(form)