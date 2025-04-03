from django.urls import path
from .views import (
    MedicationListView,
    MedicationDetailView,
    MedicationTemplateView,
    MedicationTemplateDetailView
)

urlpatterns = [
    # API endpoints
    path('api/medications/', MedicationListView.as_view(), name='medication-api-list'),
    path('api/medications/<int:pk>/', MedicationDetailView.as_view(), name='medication-api-detail'),
    
    # Template views
    path('medications/', MedicationTemplateView.as_view(), name='medication-list'),
    path('medications/<int:pk>/', MedicationTemplateDetailView.as_view(), name='medication-detail'),
]