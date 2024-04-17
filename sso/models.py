from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from sso.managers import UserManager


class User(AbstractBaseUser):
    username = models.CharField(max_length=255, default=None, blank=False, null=False, unique=True)
    name = models.CharField(max_length=255, default=None, blank=True, null=True)
    recovery_code = models.CharField(max_length=255, default=None, blank=False, null=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['name', 'password']

    def __str__(self):
        return self.username

    def has_module_perms(self, app_label):
        return self.is_superuser

    def has_perm(self, perm, obj=None):
        return self.is_superuser


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    pref_text_lang = models.CharField(max_length=255, blank=True, null=True)
    pref_voice_lang = models.CharField(max_length=255, blank=True, null=True)
    linked_x_handle = models.CharField(max_length=255, blank=True, null=True)
    linked_ig_handle = models.CharField(max_length=255, blank=True, null=True)


class UserLog(models.Model):
    result_text = models.TextField(null=True, blank=True)
    result_url = models.TextField(null=True, blank=True)
    feature_type = models.TextField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_email = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_liked = models.BooleanField(null=True, blank=False)


class Meta:
    ordering = ["-created_at"]
