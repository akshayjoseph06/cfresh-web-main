from django.db import models

from products.models import FranchiseItem
from franchise.models import Franchise

PROMO_TYPE = [
    ("PR", "Product"),
    ("CA", "Category")
]

OFFER_MODEL = [
    ('PV', 'Product Varient'),
    ('CA', 'Category'),
    ('PR', 'Product'),
]
    

class FlashSale(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    franchise_item = models.ForeignKey(FranchiseItem, on_delete=models.CASCADE)
    special_price = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'promotions_flas_sale'
        verbose_name = 'flas sale'
        verbose_name_plural = 'flas sales'
        ordering = ('-id',)

    def __str__(self):

        return self.franchise_item
    


class TodayDeal(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    franchise_item = models.ForeignKey(FranchiseItem, on_delete=models.CASCADE)
    special_price = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'promotions_today_deal'
        verbose_name = 'todays deal'
        verbose_name_plural = 'todays deals'
        ordering = ('-id',)

    def __str__(self):

        return self.franchise_item
    



class Banner(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    banner_type = models.CharField(max_length=2, choices=PROMO_TYPE)
    model_id = models.IntegerField()
    banner_image = models.FileField(null=True, blank=True)
    franchise = models.ForeignKey(Franchise, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'promotions_banner'
        verbose_name = 'banner'
        verbose_name_plural = 'banners'
        ordering = ('-id',)

    def __str__(self):

        return self.name



class Poster(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    poster_type = models.CharField(max_length=2, choices=PROMO_TYPE)
    model_id = models.IntegerField()
    poster_image = models.FileField(null=True, blank=True)
    franchise = models.ForeignKey(Franchise, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'promotions_poster'
        verbose_name = 'poster'
        verbose_name_plural = 'posters'
        ordering = ('-id',)

    def __str__(self):

        return self.name
    

class StaticBanner(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    banner_type = models.CharField(max_length=2, choices=PROMO_TYPE)
    model_id = models.IntegerField()
    banner_image = models.FileField(null=True, blank=True)
    franchise = models.ForeignKey(Franchise, null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'promotions_static_banner'
        verbose_name = 'static banner'
        verbose_name_plural = 'static banners'
        ordering = ('-id',)

    def __str__(self):

        return self.name
    


class Offer(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    offer_code = models.CharField(max_length=100)
    offer_model = models.CharField(choices=OFFER_MODEL, max_length=2)
    model_id = models.IntegerField()
    discount = models.IntegerField()
    is_percentage = models.BooleanField(default=False)
    description = models.TextField()
    maximum_discount = models.IntegerField(null=True, blank=True)
    franchise = models.ForeignKey(Franchise, null=True, blank=True, on_delete=models.CASCADE)
    

    class Meta:
        db_table = 'promotions_offer'
        verbose_name = 'offer'
        verbose_name_plural = 'offers'
        ordering = ('-id',)

    def __str__(self):

        return self.name
