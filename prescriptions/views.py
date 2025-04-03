from django.http import Http404, JsonResponse
from django.views.generic import DetailView, CreateView
from django_filters.views import FilterView
from rest_framework import generics, permissions
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from rest_framework.response import Response
from medications.models import Medication
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication
from django.views.decorators.http import require_GET
from .filters import PrescriptionFilter
from .models import Prescription
from django.views.generic import UpdateView
from .filters import PrescriptionFilter

from .serializers import PrescriptionSerializer
from .forms import PrescriptionCreateForm
from .models import Prescription, PrescriptionMedication

@require_GET
def medication_search_api(request):
    """API endpoint for searching medications."""
    search_term = request.GET.get('q', '').strip()
    
    if len(search_term) < 2:
        return JsonResponse({'results': [], 'message': 'Enter at least 2 characters'})
    
    medications = Medication.objects.filter(
        Q(name__icontains=search_term) |
        Q(dosage__icontains=search_term)
    ).values('id', 'name', 'dosage', 'presentation')[:20]
    
    results = list(medications)
    
    return JsonResponse({
        'results': results,
        'count': len(results)
    })

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

class PrescriptionUpdateView(UpdateView):
    model = Prescription
    form_class = PrescriptionCreateForm
    template_name = 'prescriptions/edit.html'
    
    def get_success_url(self):
        return reverse('prescription-list')
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_physician:
            return queryset.filter(physician=self.request.user.physician)
        return queryset.none()
    
class PrescriptionListView(FilterView):
    model = Prescription
    template_name = 'prescriptions/list.html'
    context_object_name = 'prescriptions'
    filterset_class = PrescriptionFilter
    paginate_by = 20
    
    def get_queryset(self):
        # Since Physician is the User, we can filter directly
        return Prescription.objects.filter(
            physician=self.request.user
        ).select_related('patient').order_by('-date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        context.update({
            'total_prescriptions': queryset.count(),
            'active_prescriptions': queryset.filter(is_active=True).count(),
            'inactive_prescriptions': queryset.filter(is_active=False).count(),
        })
        return context

class PrescriptionTemplateDetailView(DetailView):
    model = Prescription
    template_name = 'prescriptions/detail.html'
    context_object_name = 'prescription'

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        
        if hasattr(user, 'physician'):
            return queryset.filter(physician=user)
        elif hasattr(user, 'patient'):
            return queryset.filter(patient=user.patient)
        return queryset.none()

    def get(self, request, *args, **kwargs):
        try:
            return super().get(request, *args, **kwargs)
        except Http404:
            messages.error(request, "Prescription not found or you don't have permission to view it")
            return redirect('prescription-list')

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
        # Get the first 50 medications for initial display
        context['medications'] = Medication.objects.all().order_by('name')[:50]
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
    
class MedicationSearchAPIView(generics.ListAPIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip()
        
        if not query or len(query) < 2:
            return Response({'results': [], 'total_count': 0})
        
        medications = Medication.objects.filter(
            Q(name__icontains=query) |
            Q(dosage__icontains=query) |
            Q(composition__icontains=query) |
            Q(atc_code__icontains=query)
        ).distinct().order_by('name')[:20]
        
        results = [{
            'id': med.id,
            'name': med.name,
            'dosage': med.dosage,
            'unit': med.unit or '',
            'presentation': med.presentation,
            'public_price': str(med.public_price) if med.public_price else '',
            'text': self.format_medication_display(med)
        } for med in medications]
        
        return Response({
            'results': results,
            'total_count': len(results)
        })
    
    def format_medication_display(self, medication):
        parts = [medication.name]
        if medication.dosage:
            parts.append(f"{medication.dosage}{medication.unit or ''}")
        if medication.presentation:
            parts.append(f"({medication.presentation})")
        return ' '.join(parts)