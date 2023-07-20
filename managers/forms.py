from django import forms

from products.models import Category, Item, VariantDetail, FranchiseItem
from franchise.models import Franchise, TimeSlot
from promotions.models import FlashSale, TodayDeal, Banner, StaticBanner, Poster, Offer
from users.models import User


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name","image"]

        widgets = {
            "name":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Category Title"}),
            "image":forms.widgets.FileInput(attrs={"class": "form-control"}),
        }


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ["name","image","category","description"]

        widgets = {
            "name":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Product Title"}),
            "image":forms.widgets.FileInput(attrs={"class": "form-control"}),
            "category":forms.widgets.Select(attrs={"class": "form-control"}),
            "description":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Product Description"}),
        }



class FranchiseForm(forms.ModelForm):
    class Meta:
        model = Franchise
        fields = ["name","address","latitude","longitude","base_charge","base_distance","extra_charge","extra_distance","free_delivery_cart","delivery_distance"]

        widgets = {
            "name":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Franchise Name"}),
            "address":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Franchise Address"}),
            "latitude":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Location Latitude"}),
            "longitude":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Location Longitude"}),
            "base_charge":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Base Delivery Charge for Base Distance"}),
            "base_distance":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Base Delivery Distance in KM"}),
            "extra_distance":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Extra Distance in KM"}),
            "extra_charge":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Extra Delivery Charge per Extra Distance"}),
            "free_delivery_cart":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Free Delivery Available Cart Value"}),
            "delivery_distance":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Deliverable Distance in KM"}),
        }
    
