from django.db import models

from franchise.models import Franchise


class Category(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='category')
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'product_category'
        verbose_name = 'category'
        verbose_name_plural = 'categories'
        ordering = ('-id',)

    def __str__(self):

        return self.name
    


class Item(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    image = models.FileField(upload_to='item')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.CharField(max_length=999)
    is_active = models.BooleanField(default=True)


    class Meta:
        db_table = 'product_item'
        verbose_name = 'item'
        verbose_name_plural = 'items'
        ordering = ('-id',)

    def __str__(self):

        return self.name
    

class ItemVariant(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)


    class Meta:
        db_table = 'product_item_variant'
        verbose_name = 'item variant'
        verbose_name_plural = 'item variants'
        ordering = ('-id',)

    def __str__(self):

        return self.name
    

class VariantDetail(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    item_variant = models.ForeignKey(ItemVariant, on_delete=models.CASCADE)
    image = models.FileField(upload_to='item')
    unit = models.CharField(max_length=10)
    unit_quantity = models.FloatField(default=1)
    per_unit_price = models.IntegerField()
    net_weight = models.CharField(max_length=256)
    gross_weight = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)


    class Meta:
        db_table = 'product_variant_detail'
        verbose_name = 'variant detail'
        verbose_name_plural = 'variant details'
        ordering = ('-id',)

    def __str__(self):

        return self.name
    

class FranchiseItem(models.Model):
    created_datetime = models.DateTimeField(auto_now=True)
    franchise = models.ForeignKey(Franchise, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    variations = models.ManyToManyField(VariantDetail)
    unit = models.CharField(max_length=10)
    unit_quantity = models.FloatField(default=1)
    per_unit_price = models.IntegerField()
    sold = models.IntegerField(default=0)
    in_stock = models.IntegerField(default=0)
    net_weight = models.CharField(max_length=256)
    gross_weight = models.CharField(max_length=256)
    is_active = models.BooleanField(default=True)
    delivery_distance=models.FloatField()


    class Meta:
        db_table = 'product_franchise_item'
        verbose_name = 'franchise item'
        verbose_name_plural = 'franchise items'
        ordering = ('-id',)

    def __str__(self):

        return self.item.name
