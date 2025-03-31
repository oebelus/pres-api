from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('patients.urls')),
    path('', include('physicians.urls')),
    path('', include('medications.urls')),
    path('', include('prescriptions.urls')),
]
