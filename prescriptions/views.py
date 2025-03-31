from django.views.generic import ListView, DetailView, CreateView
from rest_framework import generics, permissions
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib import messages

from .serializers import PrescriptionSerializer, CreatePrescriptionSerializer
from .forms import MedicationSelectionForm, PrescriptionCreateForm
from .models import Prescription, PrescriptionMedication

class PrescriptionListView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreatePrescriptionSerializer
        return PrescriptionSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'physician'):
            return Prescription.objects.filter(physician=user)
        elif hasattr(user, 'patient'):
            return Prescription.objects.filter(patient=user)
        return Prescription.objects.none()

class PrescriptionDetailView(generics.RetrieveAPIView):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'physician'):
            return Prescription.objects.filter(physician=user)
        elif hasattr(user, 'patient'):
            return Prescription.objects.filter(patient=user)
        return Prescription.objects.none()
    
class PrescriptionTemplateListView(ListView):
    model = Prescription
    template_name = 'prescriptions/list.html'
    context_object_name = 'prescriptions'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'physician'):
            return Prescription.objects.filter(physician=user)
        elif hasattr(user, 'patient'):
            return Prescription.objects.filter(patient=user)
        return Prescription.objects.none()

class PrescriptionTemplateDetailView(DetailView):
    model = Prescription
    template_name = 'prescriptions/detail.html'
    context_object_name = 'prescription'

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'physician'):
            return Prescription.objects.filter(physician=user)
        elif hasattr(user, 'patient'):
            return Prescription.objects.filter(patient=user)
        return Prescription.objects.none()

class PrescriptionTemplateCreateView(CreateView):
    model = Prescription
    form_class = PrescriptionCreateForm
    template_name = 'prescriptions/create.html'
    success_url = reverse_lazy('prescription-list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medication_form'] = MedicationSelectionForm()
        return context

    def form_valid(self, form):
        prescription = form.save(commit=False)
        prescription.physician = self.request.user
        prescription.save()
        return super().form_valid(form)
    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.physician = request.user
            prescription.save()
            
            # Process medications
            medication_ids = request.POST.getlist('medications[]')
            dosage_instructions = request.POST.getlist('dosage_instructions[]')
            duration_days = request.POST.getlist('duration_days[]')
            
            for i, med_id in enumerate(medication_ids):
                PrescriptionMedication.objects.create(
                    prescription=prescription,
                    medication_id=med_id,
                    dosage_instruction=dosage_instructions[i],
                    duration_days=duration_days[i]
                )
            
            messages.success(request, 'Prescription created successfully!')
            return redirect(self.success_url)
        return self.form_invalid(form)