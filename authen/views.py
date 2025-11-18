from django.shortcuts import render
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer



class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View to obtain an access token and a refresh token for a user.
    """
    serializer_class = CustomTokenObtainPairSerializer

