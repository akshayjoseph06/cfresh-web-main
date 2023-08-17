from django import forms

from products.models import Category, Item, VariantDetail, FranchiseItem
from franchise.models import Franchise, TimeSlot
from promotions.models import FlashSale, TodayDeal, Banner, StaticBanner, Poster, Offer
from users.models import User



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","phone_number","email","password"]

        widgets = {
            "first_name":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Full Name"}),
            "phone_number":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Mobile Number"}),
            "email":forms.widgets.EmailInput(attrs={"class": "form-control","placeholder":"Email Address"}),
            "password":forms.widgets.PasswordInput(attrs={"class": "form-control","placeholder":"Password"}),
        }


class DateInput(forms.DateInput):
    input_type = 'date'

class TimeInput(forms.TimeInput):
    input_type = 'time'


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
    


class VariantDetailForm(forms.ModelForm):
    class Meta:
        model = VariantDetail
        fields = ["name","image","per_unit_price",]

        widgets = {
            "name":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Vraiant Name"}),
            "image":forms.widgets.FileInput(attrs={"class": "form-control"}),
            "per_unit_price":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Unit Price"}),
        }


class FranchiseItemForm(forms.ModelForm):
    class Meta:
        model = FranchiseItem
        fields = ["item","unit","unit_quantity","per_unit_price","net_weight","gross_weight","delivery_distance"]

        widgets = {
            "item":forms.widgets.Select(attrs={"class": "form-control"}),
            "unit":forms.widgets.Select(attrs={"class": "form-control"}),
            "unit_quantity":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Unit Quantity"}),
            "per_unit_price":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Unit Price"}),
            "net_weight":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Net Weight"}),
            "gross_weight":forms.widgets.TextInput(attrs={"class": "form-control","placeholder":"Gross Weight"}),
            "delivery_distance":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Delivery Distance"}),
        }


class FranchiseItemStockForm(forms.ModelForm):
    class Meta:
        model = FranchiseItem
        fields = ["in_stock"]

        widgets = {
            "in_stock":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Stock"}),
        }


class TimeSlotForm(forms.ModelForm):
    class Meta:
        model = TimeSlot
        fields = ["franchise","from_time","to_time",]

        widgets = {
            "franchise":forms.widgets.Select(attrs={"class": "form-control"}),
            "from_time":TimeInput(attrs={"class": "form-control"}),
            "to_time":TimeInput(attrs={"class": "form-control"}),
        }



class FlashSaleForm(forms.ModelForm):
    class Meta:
        model = FlashSale
        fields = ["franchise_item","special_price"]

        widgets = {
            "franchise_item":forms.widgets.Select(attrs={"class": "form-control"}),
            "special_price":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Special Price"}),
        }


class TodayDealForm(forms.ModelForm):
    class Meta:
        model = TodayDeal
        fields = ["franchise_item","special_price"]

        widgets = {
            "franchise_item":forms.widgets.Select(attrs={"class": "form-control"}),
            "special_price":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Special Price"}),
        }



class TodayDealForm(forms.ModelForm):
    class Meta:
        model = TodayDeal
        fields = ["franchise_item","special_price"]

        widgets = {
            "franchise_item":forms.widgets.Select(attrs={"class": "form-control"}),
            "special_price":forms.widgets.NumberInput(attrs={"class": "form-control","placeholder":"Special Price"}),
        }