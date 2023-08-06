from django.db import models
from django.db.models import JSONField

from users.models import User
    

class Franchise(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=256)
    district = models.CharField(max_length=256, default="Malappuram")
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    base_charge=models.IntegerField()
    base_distance=models.IntegerField()
    extra_charge=models.IntegerField()
    extra_distance=models.IntegerField()
    free_delivery_cart=models.FloatField(default=0)
    instant_delivery=models.BooleanField(default=True)
    delivery_distance=models.FloatField()

    class Meta:
        db_table = 'franchise_franchise'
        verbose_name = 'franchise'
        verbose_name_plural = 'franchises'
        ordering = ('-id',)

    def __str__(self):

        return self.name
    


class FranchiseUser(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)

    class Meta:
        db_table = 'franchise_franchise_user'
        verbose_name = 'franchise user'
        verbose_name_plural = 'franchise users'
        ordering = ('-id',)

    def __str__(self):

        return self.user.first_name
    


class TimeSlot(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    from_time = models.TimeField()
    to_time = models.TimeField()
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)

    class Meta:
        db_table = 'franchise_time_slot'
        verbose_name = 'time slot'
        verbose_name_plural = 'time slots'
        ordering = ('-id',)

    def __str__(self):

        return f'{self.franchise}-{self.from_time.strftime("%H:%M %p")}-{self.to_time.strftime("%H:%M %p")}'