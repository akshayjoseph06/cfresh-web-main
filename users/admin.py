from django.contrib import admin

from .models import User, OTPVerifier


admin.site.register(User)
admin.site.register(OTPVerifier)
