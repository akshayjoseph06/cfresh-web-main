import datetime
import csv
import random
from io import TextIOWrapper

from django.shortcuts import get_object_or_404, render, reverse
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect

from main.decorators import allow_manager
from main.functions import generate_form_errors

from managers.models import Manager
from products.models import Category, Item, VariantDetail, FranchiseItem
from franchise.models import FranchiseUser, Franchise, TimeSlot
from customers.models import Customer, CustomerAddress, Cart
from delivery.models import DeliveryAgent
from notifications.models import Notification
from promotions.models import FlashSale, TodayDeal, Banner, StaticBanner, Poster, Offer
from users.models import User, OTPVerifier

from managers.forms import CategoryForm, ItemForm, FranchiseForm, VariantDetailForm, FranchiseItemForm, TimeSlotForm, FlashSaleForm, TodayDealForm, FranchiseItemStockForm, UserForm


@login_required(login_url="/manager/login")
@allow_manager
def index(request):
    
    context= {
        "title": "C-FRESH | Dashboard",
    }
    return render(request, "manager/index.html", context=context)



def login(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')

        if phone_number and password:
            user = authenticate(request, phone_number=phone_number, password=password)
            if user is not None and user.is_manager:
                auth_login(request, user)

                return HttpResponseRedirect(reverse("managers:index"))
            else:
                context= {
                    "title": "Manager Login | Home",
                    "error": True,
                    "message": "Invalid credentials or not allowed user"
                }
                return render(request, "manager/login.html", context=context)
        else:
            context= {
                "title": "Manager Login | Home",
                "error": True,
                "message": "Invalid credentials or not allowed user"
            }
            return render(request, "manager/login.html", context=context)
    else:
        context= {
            "title" : "Manager Login | Home"
        }
        return render(request, "manager/login.html", context=context)
    


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse("managers:login"))



@login_required(login_url="/manager/login")
@allow_manager
def account(request):
    user=request.user
    manager= Manager.objects.get(user=user)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Profile",
        "name": "My Account",
        "manager":manager,
    }
    return render(request, "manager/account.html", context=context)



################################################################
################   Categories       ############################
################################################################


@login_required(login_url="/manager/login")
@allow_manager
def categories(request):
    user=request.user
    manager= Manager.objects.get(user=user)

    instances=Category.objects.all()
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Categories",
        "name": "Categories List",
        "manager":manager,
        "instances":instances
    }
    return render(request, "manager/categories.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def categories_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse("managers:categories"))
        else:
            message = generate_form_errors(form)
            form = CategoryForm()
            context= {
                "title": "Manager Dashboard | Add Category",
                "sub_title": "Categories",
                "name": "Add Category",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "manager/categories-add.html", context=context)

    else:
        form = CategoryForm()
        context= {
            "title": "Manager Dashboard | Add Category",
            "sub_title": "Categories",
            "name": "Add Category",
            "form": form,
        }
        return render(request, "manager/categories-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def categories_edit(request, id):
    instance=Category.objects.get(id=id)

    if request.method == "POST":
        form = CategoryForm(request.POST,request.FILES, instance=instance)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse("managers:categories"))
        else:
            message = generate_form_errors(form)
            form = CategoryForm(instance=instance)
            context= {
                "title": "Manager Dashboard | Edit Category",
                "sub_title": "Categories",
                "name": "Edit Category",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "manager/categories-add.html", context=context)

    else:
        form = CategoryForm(instance=instance)
        context= {
            "title": "Manager Dashboard | Edit Category",
            "sub_title": "Categories",
            "name": "Edit Category",
            "form": form,
            "instance": instance,
        }
        return render(request, "manager/categories-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def categories_delete(request, id):
    instance = Category.objects.get(id=id)
    instance.delete()
    
    return HttpResponseRedirect(reverse("managers:categories"))



################################################################
################   Products       ############################
################################################################


@login_required(login_url="/manager/login")
@allow_manager
def products(request):
    user=request.user
    manager= Manager.objects.get(user=user)

    instances=Item.objects.all()
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Products",
        "name": "Products List",
        "manager":manager,
        "instances":instances
    }
    return render(request, "manager/products.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def products_add(request):
    if request.method == "POST":
        form = ItemForm(request.POST,request.FILES)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse("managers:products"))
        else:
            message = generate_form_errors(form)
            form = ItemForm()
            context= {
                "title": "Manager Dashboard | Add Item",
                "sub_title": "Products",
                "name": "Add Item",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "manager/products-add.html", context=context)

    else:
        form = ItemForm()
        context= {
            "title": "Manager Dashboard | Add Item",
            "sub_title": "Products",
            "name": "Add Item",
            "form": form,
        }
        return render(request, "manager/products-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def products_edit(request, id):
    instance=Item.objects.get(id=id)
    if request.method == "POST":
        form = ItemForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse("managers:products"))
        else:
            message = generate_form_errors(form)
            form = ItemForm(instance=instance)
            context= {
                "title": "Manager Dashboard | Edit Item",
                "sub_title": "Products",
                "name": "Edit Item",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "manager/products-add.html", context=context)

    else:
        form = ItemForm(instance=instance)
        context= {
            "title": "Manager Dashboard | Edit Item",
            "sub_title": "Products",
            "name": "Edit Item",
            "instance": instance,
            "form": form,
        }
        return render(request, "manager/products-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def products_delete(request, id):
    instance = Item.objects.get(id=id)
    instance.delete()
    
    return HttpResponseRedirect(reverse("managers:products"))



################################################################
################   franchise       ############################
################################################################


@login_required(login_url="/manager/login")
@allow_manager
def franchise(request):
    user=request.user
    manager= Manager.objects.get(user=user)

    instances=Franchise.objects.all()
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Franchise",
        "name": "Franchise List",
        "manager":manager,
        "instances":instances
    }
    return render(request, "manager/franchise.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def franchise_add(request):
    if request.method == "POST":
        form = FranchiseForm(request.POST,request.FILES)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse("managers:franchise"))
        else:
            message = generate_form_errors(form)
            form = FranchiseForm()
            context= {
                "title": "Manager Dashboard | Add Franchise",
                "sub_title": "Franchise",
                "name": "Add Franchise",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "manager/franchise-add.html", context=context)

    else:
        form = FranchiseForm()
        context= {
            "title": "Manager Dashboard | Add Franchise",
            "sub_title": "Franchise",
            "name": "Add Franchise",
            "form": form,
        }
        return render(request, "manager/franchise-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def franchise_edit(request, id):
    instance=Franchise.objects.get(id=id)

    if request.method == "POST":
        form = FranchiseForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse("managers:franchise"))
        else:
            message = generate_form_errors(form)
            form = FranchiseForm(instance=instance)
            context= {
                "title": "Manager Dashboard | Edit Franchise",
                "sub_title": "Franchise",
                "name": "Edit Franchise",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "manager/franchise-add.html", context=context)

    else:
        form = FranchiseForm(instance=instance)
        context= {
            "title": "Manager Dashboard | Edit Franchise",
            "sub_title": "Franchise",
            "name": "Edit Franchise",
            "form": form,
            "instance": instance,
        }
        return render(request, "manager/franchise-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def franchise_delete(request, id):
    instance = Franchise.objects.get(id=id)
    instance.delete()
    
    return HttpResponseRedirect(reverse("managers:franchise"))


################################################################
################   Franchise Item      #########################
################################################################


@login_required(login_url="/manager/login")
@allow_manager
def franchise_items(request,id):
    user=request.user
    manager= Manager.objects.get(user=user)
    franchise=Franchise.objects.get(id=id)

    instances=FranchiseItem.objects.filter(franchise=franchise)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Franchise",
        "name": "Items List",
        "manager":manager,
        "instances":instances,
        "franchise":franchise,
    }
    return render(request, "manager/f-items.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def franchise_items_add(request, id):
    franchise=Franchise.objects.get(id=id)
    if request.method == "POST":
        form = FranchiseItemForm(request.POST,request.FILES)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.franchise=franchise
            instance.save()

            return HttpResponseRedirect(reverse("managers:franchise"))
        else:
            message = generate_form_errors(form)
            form = FranchiseItemForm()
            context= {
                "title": "Manager Dashboard | Add Item",
                "sub_title": "Franchise",
                "name": "Add Item",
                "error": True,
                "message": message,
                "form": form,
                "franchise": franchise,
            }
            return render(request, "manager/f-items-add.html", context=context)

    else:
        form = FranchiseItemForm()
        context= {
            "title": "Manager Dashboard | Add Item",
            "sub_title": "Products",
            "name": "Add Item",
            "form": form,
            "franchise": franchise,
        }
        return render(request, "manager/f-items-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def franchise_items_edit(request, id):
    instance=FranchiseItem.objects.get(id=id)
    if request.method == "POST":
        form = FranchiseItemForm(request.POST,request.FILES, instance=instance)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse("managers:franchise"))
        else:
            message = generate_form_errors(form)
            form = FranchiseItemForm(instance=instance)
            context= {
                "title": "Manager Dashboard | Edit Item",
                "sub_title": "Franchise",
                "name": "Edit Item",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "manager/f-items-add.html", context=context)

    else:
        form = FranchiseItemForm(instance=instance)
        context= {
            "title": "Manager Dashboard | Edit Item",
            "sub_title": "Products",
            "name": "Edit Item",
            "form": form,
            "instance": instance,
        }
        return render(request, "manager/f-items-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def franchise_items_delete(request, id):
    instance = FranchiseItem.objects.get(id=id)
    instance.delete()
    
    return HttpResponseRedirect(reverse("managers:franchise"))



################################################################
################   Item Variations      #########################
################################################################


@login_required(login_url="/manager/login")
@allow_manager
def variations(request, id):
    user=request.user
    manager= Manager.objects.get(user=user)
    item=FranchiseItem.objects.get(id=id)

    instances=VariantDetail.objects.filter(item=item)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Franchise",
        "name": "Variations List",
        "manager":manager,
        "instances":instances,
        "item":item,
    }
    return render(request, "manager/variations.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def variations_add(request, id):
    item=FranchiseItem.objects.get(id=id)
    franchise=item.franchise
    if request.method == "POST":
        form = VariantDetailForm(request.POST,request.FILES)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.item=item
            instance.franchise=franchise
            instance.save()

            return HttpResponseRedirect(reverse("managers:franchise"))
        else:
            message = generate_form_errors(form)
            form = VariantDetailForm()
            context= {
                "title": "Manager Dashboard | Add Variations",
                "sub_title": "Franchise",
                "name": "Add Variations",
                "error": True,
                "message": message,
                "form": form,
                "item": item,
            }
            return render(request, "manager/variations-add.html", context=context)

    else:
        form = VariantDetailForm()
        context= {
            "title": "Manager Dashboard | Add Variations",
            "sub_title": "Products",
            "name": "Add Variations",
            "form": form,
            "item": item,
        }
        return render(request, "manager/variations-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def variations_edit(request, id):
    instance=VariantDetail.objects.get(id=id)
    if request.method == "POST":
        form = VariantDetailForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse("managers:franchise"))
        else:
            message = generate_form_errors(form)
            form = VariantDetailForm(instance=instance)
            context= {
                "title": "Manager Dashboard | Edit Variations",
                "sub_title": "Franchise",
                "name": "Edit Variations",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "manager/variations-add.html", context=context)

    else:
        form = VariantDetailForm(instance=instance)
        context= {
            "title": "Manager Dashboard | Edit Variations",
            "sub_title": "Products",
            "name": "Edit Variations",
            "form": form,
            "instance": instance,
        }
        return render(request, "manager/variations-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def variations_delete(request, id):
    instance = VariantDetail.objects.get(id=id)
    instance.delete()
    
    return HttpResponseRedirect(reverse("managers:franchise"))



@login_required(login_url="/manager/login")
@allow_manager
def stocks(request,id):
    user=request.user
    manager= Manager.objects.get(user=user)

    franchise=Franchise.objects.get(id=id)

    instances=  FranchiseItem.objects.filter(franchise=franchise)
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Franchise",
        "name": "Time slots",
        "manager":manager,
        "instances":instances
    }
    return render(request, "manager/stocks.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def stocks_edit(request,id):
    instance=FranchiseItem.objects.get(id=id)
    if request.method == "POST":
        form = FranchiseItemStockForm(request.POST,request.FILES, instance=instance)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse("managers:franchise"))
        else:
            message = generate_form_errors(form)
            form = FranchiseItemStockForm(instance=instance)
            context= {
                "title": "Manager Dashboard | Edit Stock",
                "sub_title": "Franchise",
                "name": "Edit Stock",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "manager/stock-add.html", context=context)

    else:
        form = FranchiseItemStockForm(instance=instance)
        context= {
            "title": "Manager Dashboard | Edit Stock",
            "sub_title": "Products",
            "name": "Edit Stock",
            "form": form,
            "instance": instance,
        }
        return render(request, "manager/stock-add.html", context=context)




################################################################
################   Time Slots      #############################
################################################################


@login_required(login_url="/manager/login")
@allow_manager
def timeslots(request):
    user=request.user
    manager= Manager.objects.get(user=user)

    instances=TimeSlot.objects.all()
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Franchise",
        "name": "Time slots",
        "manager":manager,
        "instances":instances
    }
    return render(request, "manager/timeslots.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def timeslots_add(request):
    if request.method == "POST":
        form = TimeSlotForm(request.POST,request.FILES)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse("managers:timeslots"))
        else:
            message = generate_form_errors(form)
            form = TimeSlotForm()
            context= {
                "title": "Manager Dashboard | Add Time slots",
                "sub_title": "Time slots",
                "name": "Add Time slots",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "manager/timeslots-add.html", context=context)

    else:
        form = TimeSlotForm()
        context= {
            "title": "Manager Dashboard | Add time slots",
            "sub_title": "time slots",
            "name": "Add Time slots",
            "form": form,
        }
        return render(request, "manager/timeslots-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def timeslots_edit(request, id):
    instance = TimeSlot.objects.get(id=id)
    if request.method == "POST":
        form = TimeSlotForm(request.POST,request.FILES,instance=instance)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse("managers:timeslots"))
        else:
            message = generate_form_errors(form)
            form = TimeSlotForm(instance=instance)
            context= {
                "title": "Manager Dashboard | Add Time slots",
                "sub_title": "Time slots",
                "name": "Add Time slots",
                "error": True,
                "message": message,
                "form": form,
                "instance": instance,
            }
            return render(request, "manager/timeslots-add.html", context=context)

    else:
        form = TimeSlotForm(instance=instance)
        context= {
            "title": "Manager Dashboard | Add time slots",
            "sub_title": "time slots",
            "name": "Add Time slots",
            "form": form,
            "instance": instance,
        }
        return render(request, "manager/timeslots-add.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def timeslots_delete(request, id):
    instance = TimeSlot.objects.get(id=id)
    instance.delete()
    
    return HttpResponseRedirect(reverse("managers:timeslots"))



################################################################
################   Time Slots      #############################
################################################################


@login_required(login_url="/manager/login")
@allow_manager
def posters(request):
    user=request.user
    manager= Manager.objects.get(user=user)

    instances=TimeSlot.objects.all()
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Franchise",
        "name": "Time slots",
        "manager":manager,
        "instances":instances
    }
    return render(request, "manager/posters.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def posters_add(request):
    pass


@login_required(login_url="/manager/login")
@allow_manager
def posters_edit(request, id):
    pass


@login_required(login_url="/manager/login")
@allow_manager
def posters_delete(request, id):
    instance = TimeSlot.objects.get(id=id)
    instance.delete()
    
    return HttpResponseRedirect(reverse("managers:posters"))



################################################################
################   Users      #############################
################################################################


@login_required(login_url="/manager/login")
@allow_manager
def customers(request):
    user=request.user
    manager= Manager.objects.get(user=user)

    instances=Customer.objects.all()
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Users",
        "name": "Customers",
        "manager":manager,
        "instances":instances
    }
    return render(request, "manager/customers.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def franchise_users(request):
    user=request.user
    manager= Manager.objects.get(user=user)

    instances=FranchiseUser.objects.all()
    
    context= {
        "title": "C-FRESH | Dashboard",
        "sub_title": "Users",
        "name": "Franchise Users",
        "manager":manager,
        "instances":instances,
    }
    return render(request, "manager/f-users.html", context=context)


@login_required(login_url="/manager/login")
@allow_manager
def franchise_users_add(request):
    if request.method == "POST":
        form = UserForm(request.POST,request.FILES)
        if form.is_valid():
            instance= form.save(commit=False)
            instance.save()

            return HttpResponseRedirect(reverse("managers:products"))
        else:
            message = generate_form_errors(form)
            form = ItemForm()
            context= {
                "title": "Manager Dashboard | Add Item",
                "sub_title": "Products",
                "name": "Add Item",
                "error": True,
                "message": message,
                "form": form,
            }
            return render(request, "manager/products-add.html", context=context)

    else:
        form = ItemForm()
        context= {
            "title": "Manager Dashboard | Add Item",
            "sub_title": "Products",
            "name": "Add Item",
            "form": form,
        }
        return render(request, "manager/products-add.html", context=context)