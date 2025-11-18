from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .views import CustomTokenObtainPairView, UserProfile, ChangePasswordView

urlpatterns = [
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('user/<int:pk>/profile/',UserProfile.as_view(),name='userprofile'),
    path("user/<int:pk>/changepassword/", ChangePasswordView.as_view(), name="change-password"),
]