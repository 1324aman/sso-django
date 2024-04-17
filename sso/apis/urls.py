from django.urls import path
from sso.apis.views import (
    FirebaseSessionView, UserProfileAPI,
    UserLogsView, UserAuthentication,
)
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('login/', FirebaseSessionView.as_view(), name='firebase_session'),
    path('user_logs/', UserLogsView.as_view(), name='user_logs'),
    path('getuser/', UserProfileAPI.as_view({"get":"get_username"}), name='get-username'),
    path('user-profile/', UserProfileAPI.as_view({"get":"user_profile_get"}), name='user_profile'),
    path('user-profile/', UserProfileAPI.as_view({"post":"user_profile_post"}), name='user_profile'),
    path('sign-up/', UserAuthentication.as_view({"post":"sign_up"}), name='sign_up'),
    path('sign-in/', UserAuthentication.as_view({"post":"sign_in"}), name='sign_in'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

]
