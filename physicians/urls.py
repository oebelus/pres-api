from django.urls import path

from .views import HomeView, LogoutView, PhysicianLoginView, PhysicianLogoutView, PhysicianProfileView, PhysicianRegisterView, RegisterView, LoginView, ProfileView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('login/', PhysicianLoginView.as_view(), name='template-login'),
    path('register/', PhysicianRegisterView.as_view(), name='template-register'),
    path('logout/', PhysicianLogoutView.as_view(), name='template-logout'),
    path('profile/', PhysicianProfileView.as_view(), name='template-profile'),
    
    path('api/login/', LoginView.as_view(), name='api-login'),
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/profile/', ProfileView.as_view(), name='api-profile'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
]