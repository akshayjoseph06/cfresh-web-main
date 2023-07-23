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
from promotions.models import Banner, StaticBanner, Poster
from products.models import Category, FranchiseItem
from .serializers import FranchiseSerializer, BannerSerializer, StaticSerializer, PosterSerializer, CategorySerializer, ProductsSerializer

conn = http.client.HTTPSConnection("api.msg91.com")


@api_view(["POST"])
@permission_classes ([AllowAny])
def otp_send(request):
    
    phone_number=request.data.get('phone_number')

    phone_number = f'{91}{phone_number}'

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
            else: 
                customer=False

            response_data = {
                "status_code" : 6000,
                "data": {
                    "id": user.id,
                    "pnone_number": user.phone_number,
                    "customer":customer,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    "message": "Successfully logged in"
                },

            }

        else:
            response_data = {
            "status_code" : 6001,
            "data": {
                "message": "Invalid OTP"
            },
        }
    else:
        response_data = {
        "status_code" : 6001,
        "data": {
            "message": "Invalid OTP"
        },
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
                "data": {
                    "message": "Account Created"
                },
            }
            
        else:
            response_data = {
            "status_code" : 6001,
            "data": {
                "message": "Email already registered"
            },
        }
    else:
        response_data = {
        "status_code" : 6001,
        "data": {
            "message": "Name & Email required"
        },
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
            "message": "Franchise found",
            "franchise" :franchise,
        },
    }
    else:
        franchise =None
        response_data = {
        "status_code" : 6001,
        "data": {
            "message": "No franchise found",
            "franchise" :franchise,
        },
    }
    return Response(response_data)



@api_view(["PUT"])
@permission_classes ([IsAuthenticated])
def update_franchise(request):
    franchise=request.data.get('franchise')
    user=request.user
    customer=Customer.objects.get(user=user)
    customer.current_franchise=franchise
    customer.save()

    response_data = {
        "status_code" : 6000,
        "data": {
            "message": "Franchise updated",
            "franchise" :franchise,
        },
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
@permission_classes ([AllowAny])
def products(request,id):
    category = Category.objects.get(id=id)
    instances = FranchiseItem.objects.filter(item=category)

    context = {
        "request": request
    }
    serializer = ProductsSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": serializer.data,
    }
    return Response(response_data)

