from django.urls import path
from .views import (
    PatientListCreateView,
    PatientRetrieveView,
    PatientTemplateListView,
    PatientTemplateDetailView,
    PatientCreateView
)

urlpatterns = [
    # API endpoints
    path('api/patients/', PatientListCreateView.as_view(), name='patient-api-list'),
    path('api/patients/<int:id>/', PatientRetrieveView.as_view(), name='patient-api-detail'),
    
    # Template views
    path('patients/', PatientTemplateListView.as_view(), name='patient-list'),
    path('patients/create/', PatientCreateView.as_view(), name='patient-create'),
    path('patients/<int:pk>/', PatientTemplateDetailView.as_view(), name='patient-detail'),
]