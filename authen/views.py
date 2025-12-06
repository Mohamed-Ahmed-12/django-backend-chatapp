from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.generics import RetrieveUpdateAPIView , UpdateAPIView , CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from .serializers import CustomTokenObtainPairSerializer, UserProfileSerializer, UserRegistrationSerializer, PrivacySettingSerializer

User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    View to obtain an access token and a refresh token for a user.
    """
    serializer_class = CustomTokenObtainPairSerializer

class UserProfile(RetrieveUpdateAPIView):
    """
    View to get or update user data
    """
    queryset = User.objects.all()
    serializer_class=UserProfileSerializer
    permission_classes = [IsAuthenticated,]
    
class ChangePasswordView(UpdateAPIView):
    """
    View to update user password 
    """
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

class SignUp(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    
    def perform_create(self, serializer):
        """
        Handle file upload and user creation manually here.
        """
        pic = self.request.FILES.get("pic", None)
        user = serializer.save()  # creates user without the pic

        if pic:
            user.pic = pic
            user.save()

class ChangePrivacy(APIView):
    def post(self, request):
        user = request.user
        
        # **Use the serializer to validate and sanitize the input**
        serializer = PrivacySettingSerializer(data=request.data)
        
        if serializer.is_valid():
            # Data is valid and converted to the correct Python type (boolean)
            is_searchable = serializer.validated_data['is_searchable']
            
            # Update the field
            user.is_searchable = is_searchable
            
            # **Best practice: Use update_fields for efficiency**
            user.save(update_fields=['is_searchable']) 
            
            # Return success
            return Response(status=status.HTTP_200_OK)
        
        # If validation fails, return the specific errors provided by the serializer
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)