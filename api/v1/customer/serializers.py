from rest_framework.serializers import ModelSerializer
from rest_framework import serializers


from franchise.models import Franchise
from promotions.models import Banner, Poster, StaticBanner
from products.models import Category


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