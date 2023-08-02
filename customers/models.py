from django.db import models

from users.models import User
from franchise.models import Franchise
from products.models import FranchiseItem, VariantDetail
from promotions.models import FlashSale, TodayDeal


class CustomerAddress(models.Model):
    name = models.CharField(max_length=256, null=True, blank=True)
    phone_number = models.CharField(max_length=12, null=True, blank=True)
    address_type = models.CharField(max_length=10)
    address = models.TextField()
    street = models.CharField(max_length=100, null=True, blank=True)
    land_mark = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


    class Meta:
        db_table = 'customer_address'
        verbose_name = 'address'
        verbose_name_plural = 'addresses'
        ordering = ('-id',)

    def __str__(self):

        return self.name



class Customer(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.ManyToManyField(CustomerAddress, related_name="customer_address", blank=True)
    current_address = models.ForeignKey(CustomerAddress, on_delete=models.SET_NULL, null=True, blank=True)
    reward_points = models.IntegerField(default=0)
    wallet_amount = models.FloatField(default=0)
    current_franchise = models.ForeignKey(Franchise, on_delete=models.SET_NULL, null=True, blank=True)
    bag_value = models.IntegerField(default=0)


    class Meta:
        db_table = 'customer_customer'
        verbose_name = 'customer'
        verbose_name_plural = 'customers'
        ordering = ('-id',)

    def __str__(self):

        return self.user.phone_number
    

class Cart(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    item = models.ForeignKey(FranchiseItem, on_delete=models.CASCADE)
    today_item = models.ForeignKey(TodayDeal,on_delete=models.CASCADE, null=True, blank=True)
    flash_item = models.ForeignKey(FlashSale,on_delete=models.CASCADE, null=True, blank=True)
    varient = models.ForeignKey(VariantDetail,on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=1)


    class Meta:
        db_table = 'customer_cart'
        verbose_name = 'cart'
        verbose_name_plural = 'carts'
        ordering = ('-id',)

    def __str__(self):

        return self.customer