from django.urls import path

from .views import MedicationListView, MedicationTemplateView

urlpatterns = [
    path('api/medications/', MedicationListView.as_view(), name='medication-list'),
    path('medications/', MedicationTemplateView.as_view(), name='medication-list'),
]