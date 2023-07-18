from django import forms

from products.models import Category, Item, ItemVariant, VariantDetail, FranchiseItem
from franchise.models import Franchise, TimeSlot
from promotions.models import FlashSale, FlashSaleItems, TodayDeal, TodayDealItems, Banner, StaticBanner, Poster, Offer
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



class ItemVariantForm(forms.ModelForm):
    class Meta:
        model = ItemVariant
        fields = ["name"]

        widgets = {
            "name":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Variant Title"}),
        }
    
