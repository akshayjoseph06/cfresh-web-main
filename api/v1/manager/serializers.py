from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from users.models import User
from products.models import Category, Item
from franchise.models import Franchise, FranchiseUser


class UserSerializer(ModelSerializer):
    class Meta:
        fields = ("id","username","email","password","first_name","phone_number","is_manager")
        model = User


class CategorySerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","image")
        model = Category


class AddCategorySerializer(ModelSerializer):
    class Meta:
        fields = ("name","image")
        model = Category


class ItemSerializer(ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","name","image", "category", "description")
        model = Item

    def get_category(self, instance):
        return f'{instance.name}'
    

class ItemAddSerializer(ModelSerializer):
    category = serializers.SerializerMethodField()

    class Meta:
        fields = ("name","image", "category", "description")
        model = Item

    def get_category(self, instance):
        return f'{instance.name}'
    


class FranchiseSerializer(ModelSerializer):
    class Meta:
        fields = ("id","name","address","base_charge","base_distance","extra_charge","extra_distance","delivery_distance")
        model = Franchise


class FranchiseAddSerializer(ModelSerializer):
    class Meta:
        fields = ("name","address","latitude","longitude","base_charge","base_distance","extra_charge","extra_distance","free_delivery_cart","delivery_distance")
        model = Franchise


class FranchiseUserSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()
    franchise = serializers.SerializerMethodField()

    class Meta:
        fields = ("id","user","franchise")
        model = FranchiseUser

    def get_user(self, instance):
        request = self.context.get("request")
        user = User.objects.filter(name=instance.user)
        serializer = UserSerializer(user, context={"request": request})
        return serializer.data
    
    def get_franchise(self, instance):
        request = self.context.get("request")
        franchise = Franchise.objects.filter(name=instance.user)
        serializer = FranchiseSerializer(franchise, context={"request": request})
        return serializer.data