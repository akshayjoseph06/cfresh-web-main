from django.db import models

from users.models import User
from franchise.models import Franchise, TimeSlot



DELIVERY_TYPE = (
    ("TS", "Time Slot"),
    ("IN", "Instant")
)

class DeliveryAgent(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_type = models.CharField(choices=DELIVERY_TYPE, max_length=2)
    time_slot = models.ForeignKey(TimeSlot, null=True, blank=True, on_delete=models.SET_NULL)
    franchise = models.ForeignKey(Franchise, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = 'delivery_delivery'
        verbose_name = 'delivery'
        verbose_name_plural = 'deliverys'
        ordering = ('id',)

    def __str__(self):

        return self.user.first_name