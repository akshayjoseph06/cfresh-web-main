from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.conf import settings


from franchise.models import Franchise, TimeSlot
from promotions.models import Banner, Poster, StaticBanner, FlashSale, TodayDeal
from products.models import Category, Item, FranchiseItem, VariantDetail
from customers.models import Customer, CustomerAddress, Cart
from orders.models import Order


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

class ItemCartSerializer(ModelSerializer):

    cart_qty = serializers.SerializerMethodField()
    class Meta:
        fields = ("id","cart_qty")
        model = Cart
    
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

class VarientsSerializer(ModelSerializer):

    cart = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","name","image","per_unit_price","cart")
        model = VariantDetail

    def get_cart(self, instance):
        request = self.context.get("request")
        user=request.user
        customer = Customer.objects.get(user=user)
        if Cart.objects.filter(varient=instance,customer=customer,is_ordered=False).exists():
            cart = Cart.objects.get(varient=instance,customer=customer,is_ordered=False)
        else:
            cart= None
        serializer = ItemCartSerializer(cart, context={"request": request})
        return serializer.data


class ProductsSerializer(ModelSerializer):

    item = serializers.SerializerMethodField()
    varients = serializers.SerializerMethodField()
    cart = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","item","unit","unit_quantity","per_unit_price","net_weight","gross_weight","varients","cart")
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
    
    def get_cart(self, instance):
        request = self.context.get("request")
        user=request.user
        customer = Customer.objects.get(user=user)
        if Cart.objects.filter(item=instance,customer=customer,is_ordered=False).exists():
            cart = Cart.objects.get(item=instance,customer=customer,is_ordered=False)
        else:
            cart= None
        serializer = ItemCartSerializer(cart, context={"request": request})
        return serializer.data
    

class FlashSaleSerializer(ModelSerializer):

    franchise_item = serializers.SerializerMethodField()
    cart = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","franchise_item","special_price", "cart")
        model = FlashSale

    def get_franchise_item(self, instance):
        request = self.context.get("request")
        item = instance.franchise_item
        serializer = ProductsSerializer(item, context={"request": request})
        return serializer.data
    
    def get_cart(self, instance):
        request = self.context.get("request")
        user=request.user
        customer = Customer.objects.get(user=user)
        if Cart.objects.filter(flash_item=instance,customer=customer,is_ordered=False).exists():
            cart = Cart.objects.get(flash_item=instance,customer=customer,is_ordered=False)
        else:
            cart= None
        serializer = ItemCartSerializer(cart, context={"request": request})
        return serializer.data
    

class TodayDealSerializer(ModelSerializer):

    franchise_item = serializers.SerializerMethodField()
    cart = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","franchise_item","special_price", "cart")
        model = TodayDeal

    def get_franchise_item(self, instance):
        request = self.context.get("request")
        item = instance.franchise_item
        serializer = ProductsSerializer(item, context={"request": request})
        return serializer.data
    
    def get_cart(self, instance):
        request = self.context.get("request")
        user=request.user
        customer = Customer.objects.get(user=user)
        if Cart.objects.filter(today_item=instance,customer=customer,is_ordered=False).exists():
            cart = Cart.objects.get(today_item=instance,customer=customer,is_ordered=False)
        else:
            cart= None
        serializer = ItemCartSerializer(cart, context={"request": request})
        return serializer.data
    
    


class AddAddressSerializer(ModelSerializer):

    class Meta:
        fields = ("name","phone_number","address_type", "address", "street", "land_mark", "latitude", "longitude",)
        model = CustomerAddress


class AddressListSerializer(ModelSerializer):

    primary = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","name","phone_number","address_type", "address", "street", "land_mark","primary")
        model = CustomerAddress

    def get_primary(self, instance):
        request = self.context.get("request")
        user=request.user
        customer = Customer.objects.get(user=user)
        if customer.current_address == instance:
            primary = True
        else:
            primary = False
        return primary



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
        fields = ("id","cart_amount","cart_qty","unit", "name", "image","item_type")
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

        image_relative_url = item.image.url
    
        if request:
            full_image_url = request.build_absolute_uri(image_relative_url)
            return full_image_url
        
        return image_relative_url
    

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


class TimeSlotSerializer(ModelSerializer):

    from_time = serializers.SerializerMethodField()
    to_time = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","from_time","to_time")
        model = TimeSlot

    def get_from_time(self, obj):

        return obj.from_time.strftime('%I:%M %p')

    def get_to_time(self, obj):

        return obj.to_time.strftime('%I:%M %p')
    

class CartOrderSerializer(ModelSerializer):

    name = serializers.SerializerMethodField()
    cart_qty = serializers.SerializerMethodField()
    unit = serializers.SerializerMethodField()


    class Meta:
        fields = ("id","cart_amount","cart_qty","unit", "name")
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

class OrderSerializer(ModelSerializer):

    franchise = serializers.SerializerMethodField()
    district = serializers.SerializerMethodField()
    cart_items = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","order_id","franchise","district","cart_items","address","actual_price","offer_price","delivery_charge","final_price")
        model = Order

    
    def get_franchise(self, instance):
        request = self.context.get("request")
        franchise = instance.franchise
        return franchise.name
    
    def get_district(self, instance):
        request = self.context.get("request")
        franchise = instance.franchise
        return franchise.district
    
    def get_cart_items(self, instance):
        request = self.context.get("request")
        instances = instance.cart_items
        serializer = CartOrderSerializer(instances, many=True, context={"request": request})
        return serializer.data