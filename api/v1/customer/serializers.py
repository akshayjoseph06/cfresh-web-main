from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


from franchise.models import Franchise
from promotions.models import Banner, Poster, StaticBanner, FlashSale, TodayDeal
from products.models import Category, Item, FranchiseItem, VariantDetail


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
        fields = ("id","item","unit","unit_quantity","per_unit_price","varients")
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