import datetime
import csv
import random
from io import TextIOWrapper

from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

from main.decorators import allow_franchise
from main.functions import generate_form_errors

from managers.models import Manager
from products.models import Category, Item, VariantDetail, FranchiseItem
from franchise.models import FranchiseUser, Franchise, TimeSlot
from customers.models import Customer, CustomerAddress, Cart
from delivery.models import DeliveryAgent
from notifications.models import Notification
from promotions.models import FlashSale, TodayDeal, Banner, StaticBanner, Poster, Offer
from users.models import User


@login_required(login_url="/franchise/login")
@allow_franchise
def index(request):
    
    context= {
        "title": "C-FRESH | Dashboard",
    }
    return render(request, "franchise/index.html", context=context)



def login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if phone_number and password:
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None and user.is_franchise:
                auth_login(request, user)

                return HttpResponseRedirect(reverse("franchise:index"))
            else:
                context= {
                    "title": "franchise Login | Home",
                    "error": True,
                    "message": "Invalid credentials or not allowed user"
                }
                return render(request, "franchise/login.html", context=context)
        else:
            context= {
                "title": "franchise Login | Home",
                "error": True,
                "message": "Invalid credentials or not allowed user"
            }
            return render(request, "franchise/login.html", context=context)
    else:
        context= {
            "title" : "franchise Login | Home"
        }
        return render(request, "franchise/login.html", context=context)
    


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("franchise:login"))



@login_required(login_url="/franchise/login")
@allow_franchise
def account(request):
    user=request.user
    franchise= FranchiseUser.objects.get(user=user)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Profile",
        "name": "My Account",
        "franchise":franchise,
    }
    return render(request, "franchise/account.html", context=context)


@login_required(login_url="/franchise/login")
@allow_franchise
def items(request):
    user=request.user
    franchise= FranchiseUser.objects.get(user=user)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Profile",
        "name": "My Account",
        "franchise":franchise,
    }
    return render(request, "franchise/account.html", context=context)


@login_required(login_url="/franchise/login")
@allow_franchise
def variants(request):
    user=request.user
    franchise= FranchiseUser.objects.get(user=user)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Profile",
        "name": "My Account",
        "franchise":franchise,
    }
    return render(request, "franchise/account.html", context=context)