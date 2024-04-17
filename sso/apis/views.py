import string
import secrets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.viewsets import ViewSet
from rest_framework.authtoken.models import Token
from drf_firebase_auth.authentication import FirebaseAuthentication
from rest_framework import status
from sso.models import UserProfile, UserLog, User
from sso.apis.serializers import (
    UserProfileSerializer,
    UserLogSerializer,
    UserSignupSerializer,
    UserSignInSerializer,
)
from rest_framework_simplejwt.tokens import RefreshToken


@permission_classes([IsAuthenticated])
class UserProfileAPI(ViewSet):
    def get_username(self, request, *args, **kwargs):
        username = request.user.username
        return Response({"username": username})

    def user_profile_get(self, request, *args, **kwargs):
        user = request.user
        if request.method == "GET":
            try:
                # Retrieve user profile data
                profile = UserProfile.objects.get(user=user)
                serializer = UserProfileSerializer(profile)
                return Response(serializer.data)
            except UserProfile.DoesNotExist:
                return Response(
                    {"detail": "User profile does not exist."},
                    status=status.HTTP_404_NOT_FOUND,
                )

    def user_profile_post(self, request, *args, **kwargs):
        user = request.user
        try:
            # Update user profile data
            profile = UserProfile.objects.get(user=user)
            serializer = UserProfileSerializer(profile, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            # If the profile does not exist, create a new one
            print("If the profile does not exist, create a new one")
            serializer = UserProfileSerializer(data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FirebaseSessionView(APIView):
    authentication_classes = [FirebaseAuthentication]

    def post(self, request):
        user = request.user
        token, created = Token.objects.get_or_create(user=user)
        return Response({"token": token.key})

    def delete(self, request):
        request.user.auth_token.delete()
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_204_NO_CONTENT
        )


@permission_classes([IsAuthenticated])
class UserLogsView(APIView):
    def get(self, request):
        user = request.user
        logs = UserLog.objects.filter(user=user)
        serializer = UserLogSerializer(logs, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        data = {
            "result_text": request.data.get("result_text", None),
            "result_url": request.data.get("result_url", None),
            "feature_type": request.data.get("feature_type", None),
            "user": user.id,
            "user_email": user.email,
            "is_liked": request.data.get("is_liked", False),
        }
        serializer = UserLogSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        log_id = request.data.get("log_id", None)

        if log_id is not None:
            try:
                log = UserLog.objects.get(id=log_id, user=user)
                log.delete()
                return Response({"message": "Log deleted successfully"})
            except UserLog.DoesNotExist:
                return Response(
                    {"detail": "Log not found."}, status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Delete all logs for the authenticated user
            UserLog.objects.filter(user=user).delete()
            return Response({"message": "All logs deleted successfully"})

@permission_classes([AllowAny])
class UserAuthentication(ViewSet):
    def create_token(self, user):
        user.password = ""
        token = RefreshToken.for_user(user)
        return str(token.access_token), str(token)

    def sign_up(self, request, *args, **kwargs):
        serializer = UserSignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        access_token, refresh_token = self.create_token(user)
        response = {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "recovery_code": user.recovery_code,
            "access": access_token,
            "refresh": refresh_token,
        }
        return Response(response)

    def sign_in(self, request, *args, **kwargs):
        serializer = UserSignInSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = request.data.get("username")
        password = request.data.get("password")
        user = User.objects.filter(username=username).first()
        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect password")
        
        access_token, refresh_token = self.create_token(user)
        # token = RefreshToken.for_user(user)
        response = {
            "id": user.id,
            "name": user.name,
            "username": user.username,
            "access": access_token,
            "refresh": refresh_token,
        }
        return Response(response)
