from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from .models import User  # Import custom User model from your users app



# Register view (User registration)
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Allow unauthenticated users

    def post(self, request):
        # Expecting username, email, and password from the request body
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not email or not password:
            return Response({"error": "Username, email, and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists."}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({"error": "Email already exists."}, status=status.HTTP_400_BAD_REQUEST)

        # Create new user
        user = User.objects.create(username=username, email=email, password=make_password(password))
        user.save()

        # Create a token (using JWT or session, depending on your setup)
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            "message": "User registered successfully",
            "access_token": str(access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_201_CREATED)

# Login view (Authenticate user and return JWT token)
class LoginView(APIView):
    authentication_classes = []  # Disable authentication for this view
    permission_classes = []  # Optionally disable permission check if necessary
    

    def post(self, request):
        
        username = request.data.get("username")
        password = request.data.get("password")

        

        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
      
        user = authenticate(request, username=username, password=password)

        if user is None:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

        # Create a JWT token
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        return Response({
            "message": "Login successful",
            "access_token": str(access_token),
            "refresh_token": str(refresh)
        }, status=status.HTTP_200_OK)

# Logout view (Invalidate the token)
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Invalidate the token (simple approach, you can implement blacklist logic)
        try:
            request.user.auth_token.delete()  # If using token authentication
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
