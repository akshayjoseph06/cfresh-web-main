from django.db import models

from users.models import User


class Manager(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'manager_manager'
        verbose_name = 'manager'
        verbose_name_plural = 'managers'
        ordering = ('id',)

    def __str__(self):

        return self.user.first_name
    

class CompanyContact(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    company = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address_line1 = models.TextField()
    address_line2 = models.TextField()
    district = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    pincode = models.CharField(max_length=25)
    privacy = models.CharField(max_length=99)
    about = models.CharField(max_length=99)
    terms = models.CharField(max_length=99)
    refund = models.CharField(max_length=99)

    class Meta:
        db_table = 'manager_manager_contact'
        verbose_name = 'manager contact'
        verbose_name_plural = 'manager contacts'
        ordering = ('id',)

    def __str__(self):

        return self.company
