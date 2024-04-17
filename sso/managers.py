import string
import secrets
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, username, name=None, recovery_code=None, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(
            username=username,
            name=name,
            recovery_code=recovery_code,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, name=None, recovery_code=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        recovery_code = self.generate_recovery_code()

        return self.create_user(username, name, recovery_code, password, **extra_fields)

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
