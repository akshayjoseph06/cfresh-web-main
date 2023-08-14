from django.db import models

from franchise.models import Franchise, TimeSlot
from products.models import FranchiseItem, VariantDetail
from promotions.models import FlashSale, TodayDeal
from customers.models import Customer, CustomerAddress, Cart
from delivery.models import DeliveryAgent, DELIVERY_TYPE
from promotions.models import Offer



PAYMENT_STATUS = (
    ('TD', 'To be done'),
    ('IN', 'Initiated'),
    ('CO', 'Completed'),
    ('FA', 'Failed'),
    ('RF', 'Refused By Customer')
)

ORDER_STATUS = (
    ('IN', 'Initiated'),
    ('PL', 'Placed'),
    ('IP', 'In progress'),
    ('CO', 'Completed'),
    ('CA', 'Cancelled')
)

CANCELLED_BY_CHOICES = (
    ('CS', 'Customer'),
    ('DA', 'Delivery Agent'),
    ('FA', 'Franchise Admin')
)

PAYMENT_METHOD_CHOICES = (
    ("COD", "Cash on Delivery"),
    ("PTM", "Paytm"),
    ("WLT", "Wallet")
)

DELIVERY_DAY_CHOICES = (
    ("TD", "Today"),
    ("TM", "Tomorrow")
)

class Order(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    order_id = models.CharField(max_length=100)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    franchise = models.ForeignKey(Franchise, on_delete=models.SET_NULL, null=True, blank=True)
    cart_items = models.ManyToManyField(Cart)
    address = models.ForeignKey(CustomerAddress, on_delete=models.SET_NULL, null=True, blank=True)
    payment_method = models.CharField(max_length=3, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUS)
    order_status = models.CharField(max_length=2, choices=ORDER_STATUS)
    delivery_agent = models.ForeignKey(DeliveryAgent, on_delete=models.SET_NULL, null=True, blank=True)
    offer_applied = models.ForeignKey(Offer, on_delete=models.PROTECT, null=True, blank=True)
    actual_price = models.IntegerField()
    offer_price = models.IntegerField(default=0)
    final_price = models.IntegerField()
    cancelled_by = models.CharField(max_length=2, choices=CANCELLED_BY_CHOICES, null=True, blank=True)
    time_slot = models.ForeignKey(TimeSlot, on_delete=models.PROTECT, blank=True, null=True)
    delivery_type = models.CharField(choices=DELIVERY_TYPE, max_length=2)
    delivery_day = models.CharField(choices=DELIVERY_DAY_CHOICES, max_length=2, null=True, blank=True)
    delivery_charge = models.IntegerField(default=0)


    class Meta:
        db_table = 'orders_order'
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        ordering = ('-id',)

    def __str__(self):

        return self.order_id
