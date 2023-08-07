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
    franchise_user= FranchiseUser.objects.get(user=user)

    franchise = franchise_user.franchise

    instances = FranchiseItem.objects.filter(franchise=franchise)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Profile",
        "name": "My Account",
        "franchise":franchise,
        "instances":instances,
    }
    return render(request, "franchise/items.html", context=context)


@login_required(login_url="/franchise/login")
@allow_franchise
def variants(request):
    user=request.user
    franchise_user= FranchiseUser.objects.get(user=user)

    franchise = franchise_user.franchise

    instances = VariantDetail.objects.filter(franchise=franchise)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Profile",
        "name": "My Account",
        "franchise":franchise,
        "instances":instances,
    }
    return render(request, "franchise/variants.html", context=context)


@login_required(login_url="/franchise/login")
@allow_franchise
def flashsale(request):
    user=request.user
    franchise_user= FranchiseUser.objects.get(user=user)

    franchise = franchise_user.franchise

    instances = FlashSale.objects.filter(franchise=franchise)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Profile",
        "name": "My Account",
        "franchise":franchise,
        "instances":instances,
    }
    return render(request, "franchise/flashsale.html", context=context)


@login_required(login_url="/franchise/login")
@allow_franchise
def flashsale_delete(request, id):
    instance = FlashSale.objects.get(id=id)
    item= instance.franchise_item
    item.flash_sale = False
    item.save()
    instance.delete()
    return HttpResponseRedirect(reverse("franchise:flashsale"))


@login_required(login_url="/franchise/login")
@allow_franchise
def flashsale_add(request, id):
    user=request.user
    franchise_user= FranchiseUser.objects.get(user=user)

    franchise = franchise_user.franchise

    item = FranchiseItem.objects.get(id=id)

    if request.method == "POST":
        price = request.POST.get("price")

        flash_sale = FlashSale.objects.create(
            franchise=franchise,
            franchise_item=item,
            special_price=price,
        )
        item.flash_sale = True
        item.save()
        flash_sale.save()
        return HttpResponseRedirect(reverse("franchise:items"))
    
    else:
        context= {
            "title": "C-FRESH | Dashboard",
            "sub_title": "Profile",
            "name": "My Account",
            "franchise":franchise,
            "item": item,

        }
        return render(request, "franchise/flashsale-add.html", context=context)




@login_required(login_url="/franchise/login")
@allow_franchise
def todaysdeal(request):
    user=request.user
    franchise_user= FranchiseUser.objects.get(user=user)

    franchise = franchise_user.franchise

    instances = TodayDeal.objects.filter(franchise=franchise)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Profile",
        "name": "My Account",
        "franchise":franchise,
        "instances":instances,
    }
    return render(request, "franchise/todaysdeal.html", context=context)



@login_required(login_url="/franchise/login")
@allow_franchise
def todaysdeal_delete(request, id):
    instance = TodayDeal.objects.get(id=id)
    item = instance.franchise_item
    item.todays_deal = False
    item.save()
    instance.delete()
    return HttpResponseRedirect(reverse("franchise:todaysdeal"))



@login_required(login_url="/franchise/login")
@allow_franchise
def todaysdeal_add(request, id):
    user=request.user
    franchise_user= FranchiseUser.objects.get(user=user)

    franchise = franchise_user.franchise

    item = FranchiseItem.objects.get(id=id)

    if request.method == "POST":
        price = request.POST.get("price")

        todays_deal = TodayDeal.objects.create(
            franchise=franchise,
            franchise_item=item,
            special_price=price,
        )
        item.todays_deal = True
        item.save()
        todays_deal.save()
        return HttpResponseRedirect(reverse("franchise:items"))
    
    else:
        context= {
            "title": "C-FRESH | Dashboard",
            "sub_title": "Profile",
            "name": "My Account",
            "franchise":franchise,
            "item": item,
        }
        return render(request, "franchise/flashsale-add.html", context=context)



@login_required(login_url="/franchise/login")
@allow_franchise
def banners(request):
    user=request.user
    franchise_user= FranchiseUser.objects.get(user=user)

    franchise = franchise_user.franchise

    instances = Banner.objects.filter(franchise=franchise)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Profile",
        "name": "My Account",
        "franchise":franchise,
        "instances":instances,
    }
    return render(request, "franchise/banners.html", context=context)



@login_required(login_url="/franchise/login")
@allow_franchise
def banners_delete(request, id):
    instance = Banner.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("franchise:banners"))



@login_required(login_url="/franchise/login")
@allow_franchise
def banners_add(request, type):
    user=request.user
    franchise_user= FranchiseUser.objects.get(user=user)

    franchise = franchise_user.franchise

    if type == "PR":
        instances = FranchiseItem.objects.filter(franchise=franchise)
        product = True
        category = False
    elif type == "CA":
        instances = Category.objects.all()
        product = False
        category = True


    if request.method == "POST":
        model_id = request.POST.get("item")
        name = request.POST.get("name")
        banner = request.FILES.get("image")
        if type == "PR":
            banner = Banner.objects.create(
                franchise = franchise,
                name = name,
                model_id = model_id,
                banner_image =banner,
                banner_type= "PR",
            )
            return HttpResponseRedirect(reverse("franchise:banners"))
        elif type == "CA":
            banner = Banner.objects.create(
                franchise = franchise,
                name = name,
                model_id = model_id,
                banner_image =banner,
                banner_type= "CA",
            )
            return HttpResponseRedirect(reverse("franchise:banners"))
    else:
        context= {
            "title": "C-FRESH | Dashboard",
            "sub_title": "Profile",
            "name": "My Account",
            "franchise":franchise,
            "instances":instances,
            "product":product,
            "category":category,
        }
        return render(request, "franchise/banner-add.html", context=context)



@login_required(login_url="/franchise/login")
@allow_franchise
def posters(request):
    user=request.user
    franchise_user= FranchiseUser.objects.get(user=user)

    franchise = franchise_user.franchise

    instances = Poster.objects.filter(franchise=franchise)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Profile",
        "name": "My Account",
        "franchise":franchise,
        "instances":instances,
    }
    return render(request, "franchise/posters.html", context=context)



@login_required(login_url="/franchise/login")
@allow_franchise
def posters_delete(request, id):
    instance = Poster.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("franchise:posters"))



@login_required(login_url="/franchise/login")
@allow_franchise
def posters_add(request, type):
    user=request.user
    franchise_user= FranchiseUser.objects.get(user=user)

    franchise = franchise_user.franchise

    if type == "PR":
        instances = FranchiseItem.objects.filter(franchise=franchise)
        product = True
        category = False
    elif type == "CA":
        instances = Category.objects.all()
        product = False
        category = True


    if request.method == "POST":
        model_id = request.POST.get("item")
        name = request.POST.get("name")
        poster = request.FILES.get("image")
        if type == "PR":
            poster = Poster.objects.create(
                franchise = franchise,
                name = name,
                model_id = model_id,
                poster_image =poster,
                poster_type= "PR",
            )
            return HttpResponseRedirect(reverse("franchise:posters"))
        elif type == "CA":
            poster = Poster.objects.create(
                franchise = franchise,
                name = name,
                model_id = model_id,
                poster_image =poster,
                poster_type= "CA",
            )
            return HttpResponseRedirect(reverse("franchise:posters"))
    else:
        context= {
            "title": "C-FRESH | Dashboard",
            "sub_title": "Profile",
            "name": "My Account",
            "franchise":franchise,
            "instances":instances,
            "product":product,
            "category":category,
        }
        return render(request, "franchise/posters-add.html", context=context)


@login_required(login_url="/franchise/login")
@allow_franchise
def static(request):
    user=request.user
    franchise_user= FranchiseUser.objects.get(user=user)

    franchise = franchise_user.franchise

    instances = StaticBanner.objects.filter(franchise=franchise)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Profile",
        "name": "My Account",
        "franchise":franchise,
        "instances":instances,
    }
    return render(request, "franchise/static.html", context=context)



@login_required(login_url="/franchise/login")
@allow_franchise
def static_delete(request, id):
    instance = StaticBanner.objects.get(id=id)
    instance.delete()
    return HttpResponseRedirect(reverse("franchise:static"))



@login_required(login_url="/franchise/login")
@allow_franchise
def static_add(request, type):
    user=request.user
    franchise_user= FranchiseUser.objects.get(user=user)

    franchise = franchise_user.franchise

    if type == "PR":
        instances = FranchiseItem.objects.filter(franchise=franchise)
        product = True
        category = False
    elif type == "CA":
        instances = Category.objects.all()
        product = False
        category = True


    if request.method == "POST":
        model_id = request.POST.get("item")
        name = request.POST.get("name")
        static = request.FILES.get("image")
        if type == "PR":
            static = StaticBanner.objects.create(
                franchise = franchise,
                name = name,
                model_id = model_id,
                banner_image =static,
                banner_type= "PR",
            )
            return HttpResponseRedirect(reverse("franchise:static"))
        elif type == "CA":
            static = StaticBanner.objects.create(
                franchise = franchise,
                name = name,
                model_id = model_id,
                banner_image =static,
                banner_type= "CA",
            )
            return HttpResponseRedirect(reverse("franchise:static"))
    else:
        context= {
            "title": "C-FRESH | Dashboard",
            "sub_title": "Profile",
            "name": "My Account",
            "franchise":franchise,
            "instances":instances,
            "product":product,
            "category":category,
        }
        return render(request, "franchise/static-add.html", context=context)