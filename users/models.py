from django.db import models
from django.contrib.auth.models import AbstractUser

from .manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=100, unique=True, 
                                    error_messages={'unique': "Mobile number already exists"})
    is_manager= models.BooleanField('Is manager', default=False)
    is_franchise = models.BooleanField('Is franchise', default=False)
    is_customer = models.BooleanField('Is customer', default=False)
    is_delivery = models.BooleanField('Is delivery', default=False)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()


    class Meta:
        db_table = 'user_user'
        verbose_name = 'user'
        verbose_name_plural = 'users'
        ordering = ["-id"]

    def __str__(self):
        return self.phone_number
    


class OTPVerifier(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp = models.IntegerField()
    created_datetime = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.user.phone_number



