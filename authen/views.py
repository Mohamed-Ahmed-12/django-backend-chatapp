from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveUpdateAPIView , UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .serializers import CustomTokenObtainPairSerializer , UserProfileSerializer

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View to obtain an access token and a refresh token for a user.
    """
    serializer_class = CustomTokenObtainPairSerializer

class UserProfile(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes = [IsAuthenticated,]
    

class ChangePasswordView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated,]

    def update(self, request, *args, **kwargs):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)
