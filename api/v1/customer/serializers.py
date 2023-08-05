from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.conf import settings


from franchise.models import Franchise
from promotions.models import Banner, Poster, StaticBanner, FlashSale, TodayDeal
from products.models import Category, Item, FranchiseItem, VariantDetail
from customers.models import Customer, CustomerAddress, Cart


class FranchiseSerializer(ModelSerializer):
    class Meta:
        fields = ("id","name")
        model = Franchise


class BannerSerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","banner_type","model_id","banner_image")
        model = Banner

    
class PosterSerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","poster_type","model_id","poster_image")
        model = Poster

    
class StaticSerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","banner_type","model_id","banner_image")
        model = StaticBanner


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","image")
        model = Category


class ItemSerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","image","description")
        model = Item

class VarientsSerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","image","per_unit_price")
        model = VariantDetail


class ProductsSerializer(ModelSerializer):

    item = serializers.SerializerMethodField()
    varients = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","item","unit","unit_quantity","per_unit_price","net_weight","gross_weight","varients")
        model = FranchiseItem

    def get_item(self, instance):
        request = self.context.get("request")
        item = instance.item
        serializer = ItemSerializer(item, context={"request": request})
        return serializer.data

    def get_varients(self, instance):
        request = self.context.get("request")
        varients = VariantDetail.objects.filter(item=instance)
        serializer = VarientsSerializer(varients, many=True, context={"request": request})
        return serializer.data
    

class FlashSaleSerializer(ModelSerializer):

    franchise_item = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","franchise_item","special_price")
        model = FlashSale

    def get_franchise_item(self, instance):
        request = self.context.get("request")
        item = instance.franchise_item
        serializer = ProductsSerializer(item, context={"request": request})
        return serializer.data
    

class TodayDealSerializer(ModelSerializer):

    franchise_item = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","franchise_item","special_price")
        model = TodayDeal

    def get_franchise_item(self, instance):
        request = self.context.get("request")
        item = instance.franchise_item
        serializer = ProductsSerializer(item, context={"request": request})
        return serializer.data
    


class AddAddressSerializer(ModelSerializer):

    class Meta:
        fields = ("name","phone_number","address_type", "address", "street", "land_mark", "latitude", "longitude",)
        model = CustomerAddress


class AddressListSerializer(ModelSerializer):

    class Meta:
        fields = ("id","name","phone_number","address_type", "address", "street", "land_mark",)
        model = CustomerAddress



# class CartListSerializer(ModelSerializer):

#     name = serializers.SerializerMethodField()
#     image = serializers.SerializerMethodField()
#     cart_qty = serializers.SerializerMethodField()
#     unit = serializers.SerializerMethodField()

#     class Meta:
#         fields = ("id","name","image","cart_amount","cart_qty","unit")
#         model = Cart

#     def get_name(self, instance):
#         request = self.context.get("request")
#         if instance.item is not None:
#             item = instance.item.item
#         elif instance.today_item is not None:
#             item = instance.today_item.item.item
#         elif instance.flash_item is not None:
#             item = instance.flash_item.item.item
#         else:
#             item = instance.varient

#         name = item.name
#         return name
    
#     def get_image(self, instance):
#         request = self.context.get("request")
#         if instance.item is not None:
#             item = instance.item.item
#         elif instance.today_item is not None:
#             item = instance.today_item.item.item
#         elif instance.flash_item is not None:
#             item = instance.flash_item.item.item
#         else:
#             item = instance.varient

#         image = item.image
#         return image
    
    
#     def get_cart_qty(self, instance):
#         request = self.context.get("request")
#         cart_qty=0
#         if instance.item is not None:
#             item = instance.item
#             qty=item.unit_quantity
#             cart_qty=instance.quantity * qty
#         elif instance.today_item is not None:
#             item = instance.today_item.item
#             qty=item.unit_quantity
#             cart_qty=instance.quantity * qty
#         elif instance.flash_item is not None:
#             item = instance.flash_item.item
#             qty=item.unit_quantity
#             cart_qty=instance.quantity * qty
#         else:
#             variant = instance.varient
#             item = variant.item
#             qty=item.unit_quantity
#             cart_qty=instance.quantity * qty

#         return cart_qty
    
#     def get_unit(self, instance):
#         request = self.context.get("request")
#         if instance.item is not None:
#             item = instance.item
#         elif instance.today_item is not None:
#             item = instance.today_item.item
#         elif instance.flash_item is not None:
#             item = instance.flash_item.item
#         else:
#             varient = instance.varient
#             item = varient.item

#         unit = item.unit
#         return unit


class CartListSerializer(ModelSerializer):

    name = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    cart_qty = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()


    class Meta:
        fields = ("id","cart_amount","cart_qty","unit", "name", "image")
        model = Cart

    def get_name(self, instance):
        request = self.context.get("request")
        if instance.item is not None:
            item = instance.item.item
        elif instance.today_item is not None:
            item = instance.today_item.franchise_item.item
        elif instance.flash_item is not None:
            item = instance.flash_item.franchise_item.item
        else:
            item = instance.varient

        name = item.name
        return name

    def get_image(self, instance):
        request = self.context.get("request")
        if instance.item is not None:
            item = instance.item.item
        elif instance.today_item is not None:
            item = instance.today_item.franchise_item.item
        elif instance.flash_item is not None:
            item = instance.flash_item.franchise_item.item
        else:
            item = instance.varient

        image = request.build_absolute_uri(item.image)
        
        return image
    

    def get_cart_qty(self, instance):
        request = self.context.get("request")
        cart_qty=0
        if instance.item is not None:
            item = instance.item
            qty=item.unit_quantity
            cart_qty=instance.quantity * qty
        elif instance.today_item is not None:
            item = instance.today_item.franchise_item
            qty=item.unit_quantity
            cart_qty=instance.quantity * qty
        elif instance.flash_item is not None:
            item = instance.flash_item.franchise_item
            qty=item.unit_quantity
            cart_qty=instance.quantity * qty
        else:
            variant = instance.varient
            item = variant.item
            qty=item.unit_quantity
            cart_qty=instance.quantity * qty

        return cart_qty
    
    def get_unit(self, instance):
        request = self.context.get("request")
        if instance.item is not None:
            item = instance.item
        elif instance.today_item is not None:
            item = instance.today_item.franchise_item
        elif instance.flash_item is not None:
            item = instance.flash_item.franchise_item
        else:
            varient = instance.varient
            item = varient.item

        unit = item.unit
        return unit
