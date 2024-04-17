import string
import secrets
from rest_framework import serializers
from sso.models import UserProfile, UserLog, User
from rest_framework_simplejwt.tokens import RefreshToken


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = "__all__"


class UserLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLog
        fields = "__all__"


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["name", "username", "password"]

    def create(self, data):
        recovery_code = self.generate_recovery_code()
        user = User.objects.create(
            name=data["name"] if data.get('name') else None , username=data["username"], recovery_code=recovery_code
        )
        user.set_password(data["password"])
        user.save()
        return user
    
    def generate_recovery_code(self):
        alphabet = string.ascii_letters + string.digits
        while True:
            recovery_code = "".join(secrets.choice(alphabet) for i in range(10))
            if (
                any(c.islower() for c in recovery_code)
                and any(c.isupper() for c in recovery_code)
                and sum(c.isdigit() for c in recovery_code) >= 3
            ):
                return recovery_code

class UserSignInSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = ["username", "password"]