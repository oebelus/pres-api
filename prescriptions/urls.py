# prescriptions/urls.py
from django.urls import path
from .views import (
    PrescriptionTemplateDetailView,
    PrescriptionListView,
    PrescriptionTemplateCreateView,
    PrescriptionUpdateView,
    medication_search_api
)

urlpatterns = [
    path('prescriptions/', PrescriptionListView.as_view(), name='prescription-list'),
    path('prescriptions/create/', PrescriptionTemplateCreateView.as_view(), name='prescription-create'),
    path('prescriptions/<int:pk>/edit/', PrescriptionUpdateView.as_view(), name='prescription-edit'),
    path('prescriptions/<int:pk>/', PrescriptionTemplateDetailView.as_view(), name='prescription-detail'),
    path('api/medications/search/', medication_search_api, name='medication-search-api'),
]