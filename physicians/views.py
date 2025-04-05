from django.views.generic import TemplateView, CreateView, UpdateView
from django.contrib.auth.views import LoginView as DjangoLoginView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from rest_framework.validators import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework import authentication
from rest_framework.views import APIView
from rest_framework import permissions
from django.urls import reverse_lazy
from django.contrib import messages
from rest_framework import status

from medications.models import Medication
from patients.models import Patient
from prescriptions.models import Prescription

from .serializers import PhysicianProfileSerializer, PhysicianRegisterSerializer
from .forms import PhysicianLoginForm, PhysicianRegistrationForm, PhysicianProfileForm

User = get_user_model()

class RegisterView(APIView):
    def post(self, request):
        serializer = PhysicianRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            raise ValidationError('Please provide all required fields')

        physician = authenticate(request, email=email, password=password)
        
        if not physician:
            raise ValidationError('Invalid credentials', status.HTTP_400_BAD_REQUEST)
        
        serializer = PhysicianProfileSerializer(physician)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ProfileView(APIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        serializer = PhysicianProfileSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        serializer = PhysicianProfileSerializer(
            request.user, 
            data=request.data, 
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete the token to force a login
        request.auth.delete()
        return Response(
            {"detail": "Successfully logged out."},
            status=status.HTTP_200_OK
        )
    
class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['active_prescriptions_count'] = Prescription.objects.filter(
                physician=self.request.user,
                is_active=True
            ).count()
            
            context['medications_count'] = Medication.objects.count()
            
            context['recent_patients'] = Patient.objects.filter(physicians=self.request.user).order_by('-created_at')[:5]
            context['recent_prescriptions'] = Prescription.objects.filter(physician=self.request.user).order_by('-date')[:5]
            
        return context

class PhysicianLoginView(DjangoLoginView):
    template_name = 'registration/login.html'
    form_class = PhysicianLoginForm
    authentication_form = PhysicianLoginForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('template-profile')

class PhysicianRegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = PhysicianRegistrationForm
    success_url = reverse_lazy('template-login')

class PhysicianLogoutView(DjangoLogoutView):
    next_page = reverse_lazy('home')
    
    def dispatch(self, request, *args, **kwargs):
        # Clear session data
        request.session.flush()
        return super().dispatch(request, *args, **kwargs)

class PhysicianProfileView(UpdateView):
    template_name = 'physician/profile.html'
    form_class = PhysicianProfileForm
    success_url = reverse_lazy('template-profile')

    def get_object(self):
        return self.request.user