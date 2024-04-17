from django.contrib import admin
from drf_firebase_auth.models import FirebaseUser, FirebaseUserProvider
from .models import User


admin.site.register(User)
admin.site.register(FirebaseUser)
admin.site.register(FirebaseUserProvider)
