import random
import http.client
import json
import datetime
import requests

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from django.conf import settings
from django.db.models import Sum
from django.db.models import Q

from cfresh.settings import MAP_API
from users.models import User, OTPVerifier
from fcm_django.models import FCMDevice
from customers.models import Customer, CustomerAddress, Cart
from franchise.models import Franchise, TimeSlot
from promotions.models import Banner, StaticBanner, Poster, FlashSale, TodayDeal
from products.models import Category, FranchiseItem, VariantDetail
from managers.models import CompanyContact
from .serializers import FranchiseSerializer, BannerSerializer, StaticSerializer, PosterSerializer, CategorySerializer, ProductsSerializer, FlashSaleSerializer, TodayDealSerializer, AddressListSerializer, AddAddressSerializer, CartListSerializer, TimeSlotSerializer, OrderSerializer
from franchise.utils import haversine
from orders.models import Order
from orders import Checksum

conn = http.client.HTTPSConnection("api.msg91.com")
api_key = MAP_API
url ='https://maps.googleapis.com/maps/api/distancematrix/json?'




@api_view(["POST"])
@permission_classes ([AllowAny])
def otp_send(request):
    
    phone_number=request.data.get('phone_number')
    device_id = request.data.get('deviceID')
    device_type = request.data.get('device_type')

    if User.objects.filter(phone_number=phone_number).exists():
        user = User.objects.get(phone_number=phone_number)

        if OTPVerifier.objects.filter(user=user).exists():
            otp_verifier = OTPVerifier.objects.get(user=user)
            otp_verifier.delete()

        otp = random.randrange(100000, 999999)
        otp_verifier = OTPVerifier.objects.create(user=user, otp=otp)

        headers = {
          'authkey': settings.MSG91_AUTH_KEY,
          'content-type': "application/json"
        }
        otp = otp_verifier.otp
        customer_phone = otp_verifier.user.phone_number
        payload = {
          "sender": settings.MSG91_SENDER_ID,
          "route": "4",
          "sms": [ { "message": f"Welcome to CFRESH , Your OTP verification code is: {otp}", "to": [ customer_phone ] } ],
          "DLT_TE_ID": settings.MSG91_DLT_TE_ID
        }
        payload = json.dumps(payload)
        conn.request("POST", "/api/v2/sendsms", payload, headers)
        res = conn.getresponse()
        data = res.read()

        if device_id:
            try:
                fcm_device = FCMDevice.objects.get(user=user)
                fcm_device.delete()
            except FCMDevice.DoesNotExist:
                pass
            fcm_device = FCMDevice()
            fcm_device.registration_id = device_id
            fcm_device.user = user
            if device_type == 'ios':
                fcm_device.type = "ios"
            else:
                fcm_device.type = "android"
            fcm_device.save()

            response_data = {
                "status_code" : 6000,
                "data": {
                    "message": "OTP Send to your number",
                    "phone_number":phone_number,
                },
            }
        return Response(response_data)
        
    else:
        user= User.objects.create_user(
            phone_number=phone_number,
            password="Password@123",
            is_customer=True,
        )
        otp = random.randrange(100000, 999999)
        otp_verifier = OTPVerifier.objects.create(user=user, otp=otp)

        headers = {
          'authkey': settings.MSG91_AUTH_KEY,
          'content-type': "application/json"
        }
        otp = otp_verifier.otp
        customer_phone = otp_verifier.user.phone_number
        payload = {
          "sender": settings.MSG91_SENDER_ID,
          "route": "4",
          "sms": [ { "message": f"Welcome to CFRESH , Your OTP verification code is: {otp}", "to": [ customer_phone ] } ],
          "DLT_TE_ID": settings.MSG91_DLT_TE_ID
        }
        payload = json.dumps(payload)
        conn.request("POST", "/api/v2/sendsms", payload, headers)
        res = conn.getresponse()
        data = res.read()

        if device_id:
            try:
                fcm_device = FCMDevice.objects.get(user=user)
                fcm_device.delete()
            except FCMDevice.DoesNotExist:
                pass
            fcm_device = FCMDevice()
            fcm_device.registration_id = device_id
            fcm_device.user = user
            if device_type == 'ios':
                fcm_device.type = "ios"
            else:
                fcm_device.type = "android"
            fcm_device.save()

            response_data = {
                "status_code" : 6000,
                "data": {
                    "message": "OTP Send to your number",
                    "phone_number":phone_number,
                },
            }

        return Response(response_data)


@api_view(["POST"])
@permission_classes ([AllowAny])
def otp_verify(request):
    phone_number=request.data.get('phone_number')
    otp=request.data.get('otp')

    if phone_number and otp:
        user=User.objects.get(phone_number=phone_number)
        if OTPVerifier.objects.filter(user=user, otp=otp).exists():
            otp_verifier=OTPVerifier.objects.get(user=user)
            refresh = RefreshToken.for_user(user)
            if Customer.objects.filter(user=user).exists():
                customer=True
                cs=Customer.objects.get(user=user)
                if cs.current_franchise is not None:
                    franchise = cs.current_franchise.name
                    district=cs.current_franchise.district
                    fr=True
                else:
                    franchise =None
                    district=None
                    fr=False
            else: 
                customer=False
                franchise =None
                district=None
                fr=False

            response_data = {
                "status_code" : 6000,
                "data": {
                    "id": user.id,
                    "pnone_number": user.phone_number,
                    "customer":customer,
                    "franchise":franchise,
                    "district":district,
                    "fr":fr,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                },
                "message": "Successfully logged in"

            }

        else:
            response_data = {
            "status_code" : 6001,
            "data": {},
            "message": "Invalid OTP"
        }
    else:
        response_data = {
        "status_code" : 6001,
        "data": {},
        "message": "Invalid OTP"
    }
    return Response(response_data)


@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def register(request):
    user=request.user
    first_name=request.data.get('full_name')
    email=request.data.get('email')

    if first_name and email:
        if not User.objects.filter(email=email).exists():
            user.first_name=first_name
            user.email=email
            user.save()
            customer = Customer.objects.create(
                user=user,
            )
            customer.save()
            response_data = {
                "status_code" : 6000,
                "data": {},
                "message": "Account Created",
            }
            
        else:
            response_data = {
            "status_code" : 6001,
            "data": {},
            "message": "Email already registered",
        }
    else:
        response_data = {
        "status_code" : 6001,
        "data": {},
        "message": "Name & Email required"
    }
    
    return Response(response_data)


@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def check_franchise(request):
    user=request.user
    customer=Customer.objects.get(user=user)

    if customer.current_franchise is not None:
        franchise = customer.current_franchise
        response_data = {
        "status_code" : 6000,
        "data": {
            "franchise" :franchise,
            "fr" :True,
        },
        "message": "Franchise found",
    }
    else:
        franchise =None
        response_data = {
        "status_code" : 6001,
        "data": {
            "franchise" :franchise,
            "fr" :False,
        },
        "message": "No franchise found",
    }
    return Response(response_data)



@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def update_franchise(request):
    franchise=request.data.get('franchise')
    franchise=Franchise.objects.get(id=franchise)
    user=request.user
    customer=Customer.objects.get(user=user)
    customer.current_franchise=franchise
    customer.save()

    fr=customer.current_franchise.name
    district=customer.current_franchise.district

    response_data = {
        "status_code" : 6000,
        "data": {
            "franchise" :fr,
            "district" :district,
        },
        "message": "Franchise updated",
    }
    return Response(response_data)


@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def list_franchise(request):
    instances = Franchise.objects.all()
    context = {
        "request": request
    }
    serializer = FranchiseSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": serializer.data,
    }
    return Response(response_data)



@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def banner(request):
    user=request.user
    customer = Customer.objects.get(user=user)
    franchise= customer.current_franchise
    instances = Banner.objects.filter(franchise=franchise)

    context = {
        "request": request
    }
    serializer = BannerSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": serializer.data,
    }
    return Response(response_data)



@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def poster(request):
    user=request.user
    customer = Customer.objects.get(user=user)
    franchise= customer.current_franchise
    instances = Poster.objects.filter(franchise=franchise)

    context = {
        "request": request
    }
    serializer = PosterSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": serializer.data,
    }
    return Response(response_data)



@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def static(request):
    user=request.user
    customer = Customer.objects.get(user=user)
    franchise= customer.current_franchise
    instances = StaticBanner.objects.filter(franchise=franchise)

    context = {
        "request": request
    }
    serializer = StaticSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": serializer.data,
    }
    return Response(response_data)


@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def categories(request):
    instances = Category.objects.all()

    context = {
        "request": request
    }
    serializer = CategorySerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": serializer.data,
    }
    return Response(response_data)


@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def flash_sale(request):
    user=request.user
    customer = Customer.objects.get(user=user)
    franchise= customer.current_franchise
    instances = FlashSale.objects.filter(franchise=franchise)

    context = {
        "request": request
    }
    serializer = FlashSaleSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": serializer.data,
    }
    return Response(response_data)


@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def todays_deal(request):
    user=request.user
    customer = Customer.objects.get(user=user)
    franchise= customer.current_franchise
    instances = TodayDeal.objects.filter(franchise=franchise)

    context = {
        "request": request
    }
    serializer = TodayDealSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": serializer.data,
    }
    return Response(response_data)



@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def products(request,id):
    user=request.user
    customer = Customer.objects.get(user=user)
    franchise= customer.current_franchise
    category = Category.objects.get(id=id)
    instances = FranchiseItem.objects.filter(item__category=category,franchise=franchise)

    cat_id = category.id

    context = {
        "request": request
    }
    serializer = ProductsSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "category_id": cat_id,
        "data": serializer.data,
    }
    return Response(response_data)



@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def address(request):
    user=request.user
    customer = Customer.objects.get(user=user)
    instances = customer.address
    
    current_address= customer.current_address

    context = {
        "request": request
    }
    serializer = AddressListSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": {
            "address": serializer.data,
        }
    }
    return Response(response_data)



@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def address_add(request):
    user=request.user
    customer = Customer.objects.get(user=user)

    serializer = AddAddressSerializer(data=request.data)

    if serializer.is_valid():
        instance = serializer.save()

        customer.current_address=instance
        customer.address.add(instance)
        customer.save()

        response_data = {
                "staus_code": 6000,
                "data": serializer.data,
                "status":"Address Added",
            }
        
    else:
        response_data = {
            "staus_code": 6001,
            "data": serializer.data,
            "status":"Error Occured."
        }

    return Response(response_data)


@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def address_delete(request, id):

    user=request.user
    customer = Customer.objects.get(user=user)

    address_count = customer.address.count()
    instance = CustomerAddress.objects.get(id=id)

    if address_count == 1:
        instance.delete()
    elif address_count == 2:
        instance.delete()
        address = customer.address
        customer.current_address = address
        customer.save()
    else:
        if customer.current_address == instance:
            instance.delete()
            address = customer.address[0]
            customer.current_address = address
            customer.save()
        else:
            instance.delete()

    response_data = {
        "staus_code": 6000,
        "data": {},
        "status":"Address Deleted"
    }

    return Response(response_data)


@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def address_primary(request, id):

    user=request.user
    customer = Customer.objects.get(user=user)

    instance = CustomerAddress.objects.get(id=id)

    customer.current_address = instance

    customer.save()

    response_data = {
        "staus_code": 6000,
        "data": {},
        "status":"Current Address Changed"
    }

    return Response(response_data)



@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def cart(request):

    user=request.user
    customer = Customer.objects.get(user=user)

    franchise = customer.current_franchise

    instances = Cart.objects.filter(franchise=franchise, customer=customer, is_ordered=False)

    items_count = Cart.objects.filter(franchise=franchise, customer=customer, is_ordered=False).count()

    items_total = instances.aggregate(Sum('cart_amount'))["cart_amount__sum"]


    context = {
        "request": request
    }

    serializer = CartListSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": {
            "items": serializer.data,
            "items_count": items_count,
            "items_total": items_total,
        },
    }
    return Response(response_data)



@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def cart_add(request):
    user=request.user
    customer = Customer.objects.get(user=user)

    franchise = customer.current_franchise

    lat1 = franchise.latitude
    long1 = franchise.longitude
    delivery_distance = franchise.delivery_distance

    item_type=request.data.get('item_type')
    item_id = request.data.get('item_id')

    if item_type == 'FI':
        item = FranchiseItem.objects.get(id=item_id)
        cart_amount = item.per_unit_price
    elif item_type == 'VR':
        variant = VariantDetail.objects.get(id=item_id)
        item = variant.item
        cart_amount = variant.per_unit_price
    elif item_type == 'TD':
        todays_deal = TodayDeal.objects.get(id=item_id)
        item = todays_deal.franchise_item
        cart_amount = todays_deal.special_price
    elif item_type == 'FS':
        flash_sale = FlashSale.objects.get(id=item_id)
        item = flash_sale.franchise_item
        cart_amount = flash_sale.special_price

    if item.delivery_distance > 0:
        delivery_distance = item.delivery_distance

    if customer.current_address is not None:
        address = customer.current_address
        lat2 = address.latitude
        long2 = address.longitude

        distance = haversine(long2, lat2, long1, lat1)

        if distance < delivery_distance :
            if item_type == 'FI':
                cart = Cart.objects.create(
                    customer=customer,
                    franchise=franchise,
                    item=item,
                    item_type=item_type,
                    cart_amount=cart_amount,
                    quantity=1,
                )
            elif item_type == 'VR':
                cart = Cart.objects.create(
                    customer=customer,
                    franchise=franchise,
                    varient=variant,
                    item_type=item_type,
                    cart_amount=cart_amount,
                    quantity=1,
                )
            elif item_type == 'TD':
                cart = Cart.objects.create(
                    customer=customer,
                    franchise=franchise,
                    today_item=todays_deal,
                    item_type=item_type,
                    cart_amount=cart_amount,
                    quantity=1,
                )
            elif item_type == 'FS':
                cart = Cart.objects.create(
                    customer=customer,
                    franchise=franchise,
                    flash_item=flash_sale,
                    item_type=item_type,
                    cart_amount=cart_amount,
                    quantity=1,
                )

            response_data = {
                "staus_code": 6000,
                "data": {},
                "message": "Successfully added to cart",

            }

        else:
            response_data = {
                "staus_code": 6001,
                "data": {},
                "message": "Item is not deliverable in your area. Please change your address.",

            }
    else:
        response_data = {
            "staus_code": 6002,
            "data": {},
            "message": "Delvery address not found. Please add a delivery address."
        }

    return Response(response_data)



@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def cart_plus(request):
    user=request.user
    customer = Customer.objects.get(user=user)

    cart_id = request.data.get('cart_id')

    cart = Cart.objects.get(id=cart_id)

    item_type = cart.item_type

    if item_type == 'FI':
        item = cart.item
        cart_amount = item.per_unit_price
        cart.cart_amount += cart_amount
        cart.quantity += 1
    elif item_type == 'VR':
        variant = cart.varient
        item = variant.item
        cart_amount = variant.per_unit_price
        cart.cart_amount += cart_amount
        cart.quantity += 1
    elif item_type == 'TD':
        todays_deal = cart.today_item
        item = todays_deal.franchise_item
        cart_amount = todays_deal.special_price
        cart.cart_amount += cart_amount
        cart.quantity += 1
    elif item_type == 'FS':
        flash_sale = cart.flash_item
        item = flash_sale.franchise_item
        cart_amount = flash_sale.special_price
        cart.cart_amount += cart_amount
        cart.quantity += 1

    cart.save()

    response_data = {
        "staus_code": 6000,
        "data": {
            "message": "Cart updated successfully"
        },
    }
    return Response(response_data)


@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def cart_minus(request):
    user=request.user
    customer = Customer.objects.get(user=user)

    cart_id = request.data.get('cart_id')

    cart = Cart.objects.get(id=cart_id)

    cart.quantity -= 1

    item_type = cart.item_type

    if cart.quantity == 0:
        cart.delete()

    else:

        if item_type == 'FI':
            item = cart.item
            cart_amount = item.per_unit_price
            cart.cart_amount -= cart_amount
        elif item_type == 'VR':
            variant = cart.varient
            item = variant.item
            cart_amount = variant.per_unit_price
            cart.cart_amount -= cart_amount
        elif item_type == 'TD':
            todays_deal = cart.today_item
            item = todays_deal.franchise_item
            cart_amount = todays_deal.special_price
            cart.cart_amount -= cart_amount
        elif item_type == 'FS':
            flash_sale = cart.flash_item
            item = flash_sale.franchise_item
            cart_amount = flash_sale.special_price
            cart.cart_amount -= cart_amount

        cart.save()

    response_data = {
        "staus_code": 6000,
        "data": {
            "message": "Cart updated successfully"
        },
    }
    return Response(response_data)



@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def time_slot(request):
    user=request.user
    customer = Customer.objects.get(user=user)

    franchise = customer.current_franchise

    instances = TimeSlot.objects.filter(franchise=franchise)

    today = TimeSlot.objects.filter(franchise=franchise).filter(Q(from_time__gt=datetime.datetime.now()))

    if franchise.instant_delivery == True:
        instant = True
    else:
        instant = False

    context = {
        "request": request
    }

    serializer = TimeSlotSerializer(instances, many=True,context=context)
    today = TimeSlotSerializer(today, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": {
            "instant_delivery": instant,
            "today": today.data,
            "tomorrow": serializer.data,
        },
    }
    return Response(response_data)



@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def address_select(request):
    user=request.user
    customer = Customer.objects.get(user=user)

    franchise = customer.current_franchise

    lat1 = franchise.latitude
    long1 = franchise.longitude
    delivery_distance = franchise.delivery_distance

    address=request.data.get('address')

    address = CustomerAddress.objects.get(id=address)

    lat2 = address.latitude
    long2 = address.longitude

    distance = haversine(long2, lat2, long1, lat1)

    if distance < delivery_distance:
        response_data = {
            "staus_code": 6000,
            "data": {
                "message": "Item is deliverable.",
            },
        }
    else:
        response_data = {
            "staus_code": 6001,
            "data": {
                "title": "Change Delivery Address",
                "message": "Item is not deliverable in your area. Please change your address.",
            },
        }

    return Response(response_data)


@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def checkout(request):
    user=request.user
    customer = Customer.objects.get(user=user)

    franchise = customer.current_franchise

    wallet = customer.wallet_amount

    address = customer.current_address

    delivery_type = request.data.get('delivery_type')
    delivery_day = request.data.get('delivery_day')
    time_slot = request.data.get('time_slot')

    context = {
        "request": request
    }

    address_data = AddressListSerializer(address, context=context)


    if delivery_type == "IN":
        time_slot = "Instant Delivery"
        delivery_day= "Today"
    else:
        time_slot_data = TimeSlot.objects.get(id=time_slot)
        time_slot = TimeSlotSerializer(time_slot_data, context=context)
        if delivery_day == "TD":
            delivery_day= "Today"
        else:
            delivery_day= "Tomorrow"

    lat1 = franchise.latitude
    long1 = franchise.longitude
    delivery_distance = franchise.delivery_distance
    base_charge=franchise.base_charge
    base_distance=franchise.base_distance
    extra_charge=franchise.extra_charge
    extra_distance=franchise.extra_distance

    instances = Cart.objects.filter(franchise=franchise, customer=customer, is_ordered=False)

    items_total = instances.aggregate(Sum('cart_amount'))["cart_amount__sum"]
    

    lat2 = address.latitude
    long2 = address.longitude

    distance = haversine(long2, lat2, long1, lat1)

    previous = Order.objects.all().first()

    if previous is not None:
        id = previous.id
        order_id = f'ORD000{id+1}'       
    else:
        order_id = "ORD0001"

    if distance < delivery_distance:
        req = requests.get(url + f'origins={lat2}%2C{long2}&destinations={lat1}%2C{long1}&key={api_key}')
        res = req.json()
        distance = res['rows'][0]['elements'][0]['distance']['value']
        distance = round(distance / 1000)

        if distance > base_distance:
            extra_dist = distance - base_distance
            extra_charge = (extra_dist/extra_distance) * extra_charge
            delivery_charge = extra_charge + base_charge
        else:
            delivery_charge = base_charge
        
        if delivery_type == "IN":
            response_data = {
                "staus_code": 6000,
                "data": {
                    "delivery_charge": delivery_charge,
                    "sub_total": items_total,
                    "total_amount": items_total + delivery_charge,
                    "instant_delivery":True,
                    "time_slot": {},
                    "delivery_day": delivery_day,
                    "wallet": wallet,
                    "address": address_data.data,
                    "cust_id": customer.user.phone_number,
                    "ord_id": order_id,
                },
            }
        else:
            response_data = {
                "staus_code": 6000,
                "data": {
                    "delivery_charge": delivery_charge,
                    "sub_total": items_total,
                    "total_amount": items_total + delivery_charge,
                    "instant_delivery":False,
                    "time_slot": time_slot.data,
                    "delivery_day": delivery_day,
                    "wallet": wallet,
                    "address": address_data.data,
                    "cust_id": customer.user.phone_number,
                    "ord_id": order_id,
                },
            }
    else:
        response_data = {
            "staus_code": 6001,
            "data": {
                "title": "Change Delivery Address",
                "message": "Item is not deliverable in your area. Please change your address.",
            },
        }

    return Response(response_data)



@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def account(request):
    user=request.user
    customer = Customer.objects.get(user=user)

    contact = CompanyContact.objects.all()[:1].get()

    response_data = {
        "staus_code": 6000,
        "data": {
            "customer": {
                "name":customer.user.first_name,
                "phone_number":customer.user.phone_number,
                "email":customer.user.email
                },
            "contact": {
                "company":contact.company,
                "address_line1":contact.address_line1,
                "address_line2":contact.address_line2,
                "district":contact.district,
                "state":contact.district,
                "pincode":contact.pincode,
                "phone_number":contact.number,
                "email":contact.email,
                },
            "pages": {
                "about":contact.about,
                "privacy":contact.privacy,
                "terms":contact.terms,
                "return and refund":contact.refund,
                },
        },
        "message":"Account Details"
    }
    return Response(response_data)




@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def place_order(request):
    user=request.user
    customer = Customer.objects.get(user=user)

    franchise = customer.current_franchise

    wallet = customer.wallet_amount

    address = customer.current_address

    delivery_type = request.data.get('delivery_type')
    delivery_day = request.data.get('delivery_day')
    time_slot = request.data.get('time_slot')
    delivery_charge = request.data.get('delivery_charge')
    final_price = request.data.get('final_price')
    payment_method = request.data.get('payment_method')

    delivery_charge = round(float(delivery_charge))
    delivery_charge= int(delivery_charge)

    final_price = round(float(final_price))
    final_price=int(final_price)

    previous = Order.objects.all().first()

    if delivery_type == "IN":
        time_slot = None
        delivery_day= "TD"
    else:
        time_slot = TimeSlot.objects.get(id=time_slot)

    if previous is not None:
        id = previous.id
        order_id = f'ORD000{id+1}'       
    else:
        order_id = "ORD0001"

    if payment_method == "COD":
        cart_items = Cart.objects.filter(franchise=franchise, customer=customer, is_ordered=False)
        order = Order.objects.create(
            order_id=order_id,
            customer=customer,
            franchise=franchise,
            address=address,
            payment_method=payment_method,
            payment_status="TD",
            order_status="PL",
            actual_price=final_price,
            final_price=final_price,
            time_slot=time_slot,
            delivery_type=delivery_type,
            delivery_day=delivery_day,
            delivery_charge=delivery_charge,
        )

        for item in cart_items:
            order.cart_items.add(item)
            item.is_ordered = True
            item.save()

        response_data = {
            "staus_code": 6000,
            "param_dict": {},
            "message": "Order Placed",

        }

        return Response(response_data)


    elif payment_method == "PTM":
        cart_items = Cart.objects.filter(franchise=franchise, customer=customer, is_ordered=False)
        order = Order.objects.create(
            order_id=order_id,
            customer=customer,
            franchise=franchise,
            address=address,
            payment_method=payment_method,
            payment_status="TD",
            order_status="IN",
            actual_price=final_price,
            final_price=final_price,
            time_slot=time_slot,
            delivery_type=delivery_type,
            delivery_day=delivery_day,
            delivery_charge=delivery_charge,
        )

        for item in cart_items:
            order.cart_items.add(item)
            item.is_ordered = True
            item.save()

        protocol = "http://"
        if request.is_secure():
            protocol = "https://"

        host = request.get_host()

        callback = protocol + host + "/api/v1/customer/order/payment/"

        param_dict = {
            'MID': 'PtkJAE93180656066727',
            'ORDER_ID': str(order_id),
            'TXN_AMOUNT': str(final_price),
            'CUST_ID': customer.user.phone_number,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WAP',
            'CALLBACK_URL': callback,
            # this is the url of handlepayment function, paytm will send a POST request to the fuction associated with this CALLBACK_URL
        }
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(param_dict, '4GVUX#0vvTNOqbFB')

        response_data = {
            "staus_code": 6001,
            "param_dict": param_dict,
            "message": "Order Initiated",

        }

        return Response(response_data)
    


@api_view(["POST"])
@permission_classes ([AllowAny])
def handle_payment(request):
    checksum = ""
    form = request.POST

    response_dict = {}
    order = None  # initialize the order varible with None

    for i in form.keys():
        response_dict[i] = form[i]
        if i == 'CHECKSUMHASH':
            # 'CHECKSUMHASH' is coming from paytm and we will assign it to checksum variable to verify our paymant
            checksum = form[i]

        if i == 'ORDER_ID':
            # we will get an order with id==ORDERID to turn isPaid=True when payment is successful
            order = Order.objects.get(order_id=form[i])

    # we will verify the payment using our merchant key and the checksum that we are getting from Paytm request.POST
    verify = Checksum.verify_checksum(response_dict, "4GVUX#0vvTNOqbFB", checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            order.order_status = "PL"
            order.payment_status= "CO"
            order.save()
            response_data = {
                "staus_code": 6000,
                "data": {},
                "message": "Order Placed.",

            }

            return Response(response_data)
        else:
            order.order_status = "CA"
            order.payment_status= "FA"
            order.save()
            response_data = {
                "staus_code": 6001,
                "data": {},
                "message": "Order Failed.",

            }

            return Response(response_data)    


@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def orders(request):
    user=request.user
    customer = Customer.objects.get(user=user)
    
    instances = Order.objects.filter(customer=customer)
    

    context = {
        "request": request
    }
    serializer = OrderSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data":  serializer.data,
    }
    return Response(response_data)
