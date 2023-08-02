import random
import http.client
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate
from django.conf import settings

from users.models import User, OTPVerifier
from customers.models import Customer, CustomerAddress
from franchise.models import Franchise
from promotions.models import Banner, StaticBanner, Poster, FlashSale, TodayDeal
from products.models import Category, FranchiseItem
from .serializers import FranchiseSerializer, BannerSerializer, StaticSerializer, PosterSerializer, CategorySerializer, ProductsSerializer, FlashSaleSerializer, TodayDealSerializer, AddressListSerializer, AddAddressSerializer

conn = http.client.HTTPSConnection("api.msg91.com")


@api_view(["POST"])
@permission_classes ([AllowAny])
def otp_send(request):
    
    phone_number=request.data.get('phone_number')

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

        response_data = {
            "status_code" : 6000,
            "data": {
                "message": "OTP Send to your number",
                "phone_number":phone_number,
            },
        }

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
    category = Category.objects.get(id=id)
    instances = FranchiseItem.objects.filter(item__category=category)

    context = {
        "request": request
    }
    serializer = ProductsSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
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
    current = AddressListSerializer(current_address, context=context)

    response_data = {
        "staus_code": 6000,
        "data": {
            "address": serializer.data,
            "current":current.data,
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

    instance = CustomerAddress.objects.get(id=id)

    instance.delete()

    response_data = {
        "staus_code": 6001,
        "data": [],
        "status":"Address Deleted"
    }

    return Response(response_data)



