import django_filters
from django import forms
from django.db.models import Q
from .models import Prescription

class PrescriptionFilter(django_filters.FilterSet):
    patient = django_filters.CharFilter(
        method='filter_patient_name',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by patient name...',
            'class': 'form-control'
        })
    )
    
    date = django_filters.DateFromToRangeFilter(
        field_name='date',
        label='Date Range',
        widget=django_filters.widgets.RangeWidget(attrs={
            'type': 'date',
            'class': 'form-control'
        }))
    
    status = django_filters.BooleanFilter(
        field_name='is_active',
        label='Status',
        widget=forms.Select(choices=[
            ('', 'All Statuses'),
            (True, 'Active'),
            (False, 'Inactive')
        ], attrs={'class': 'form-select'}))
    
    medication = django_filters.CharFilter(
        field_name='prescriptionmedication__medication__name',
        lookup_expr='icontains',
        widget=forms.TextInput(attrs={
            'placeholder': 'Search by medication...',
            'class': 'form-control'
        }))

    def filter_patient_name(self, queryset, name, value):
        if value:
            return queryset.filter(
                Q(patient__first_name__icontains=value) |
                Q(patient__last_name__icontains=value))
        return queryset

    class Meta:
        model = Prescription
        fields = []