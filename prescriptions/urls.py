from django.urls import path

from .views import PrescriptionListView, PrescriptionDetailView, PrescriptionTemplateCreateView, PrescriptionTemplateDetailView, PrescriptionTemplateListView

urlpatterns = [
    path('', PrescriptionTemplateListView.as_view(), name='prescription-list'),
    path('<int:pk>/', PrescriptionTemplateDetailView.as_view(), name='prescription-detail'),
    path('create/', PrescriptionTemplateCreateView.as_view(), name='prescription-create'),
    
    path('api/prescriptions/', PrescriptionListView.as_view(), name='prescription-list-api'),
    path('api/prescriptions/<int:pk>/', PrescriptionDetailView.as_view(), name='prescription-detail-api'),
]