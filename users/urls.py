from django.urls import path
from .views import RegisterView, LoginView, LogoutView

urlpatterns = [
    # URL for user registration (signup)
    path('register/', RegisterView.as_view(), name='register'),
    
    # URL for user login
    path('login/', LoginView.as_view(), name='login'),
    
    # URL for user logout
    path('logout/', LogoutView.as_view(), name='logout'),
]
