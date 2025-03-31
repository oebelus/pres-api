from django.urls import path

from .views import PatientCreateView, PatientListCreateView, PatientRetrieveView, PatientTemplateDetailView, PatientTemplateListView

urlpatterns = [
    path('patients/', PatientTemplateListView.as_view(), name='patient-list'),
    path('patients/<int:pk>/', PatientTemplateDetailView.as_view(), name='patient-detail'),
    path('patients/create/', PatientCreateView.as_view(), name='patient-create'), 
    
    path('api/patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('api/patients/<int:id>/', PatientRetrieveView.as_view(), name='patient-retrieve'),
]