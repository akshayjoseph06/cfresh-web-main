from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate

from .serializers import CategorySerializer, AddCategorySerializer, ItemSerializer, ItemAddSerializer, FranchiseSerializer, FranchiseUserSerializer, UserSerializer, FranchiseAddSerializer
from users.models import User
from products.models import Category, Item
from franchise.models import Franchise, FranchiseUser


@api_view(["POST"])
@permission_classes ([AllowAny])
def login(request):

    username=request.POST.get('username')
    password=request.POST.get('password')

    if username and password:
        user = authenticate(request, username=username, password=password)

        if user.is_manager:
            refresh = RefreshToken.for_user(user)


            response_data = {
                "status_code" : 6000,
                "data": {
                    "id": user.id,
                    "username" : user.username,
                    "name" : user.first_name,
                    "email" : user.email,
                    "pnone_number": user.phone_number,
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    "message": "Successfully logged in"
                },

            }
        
        else:
            response_data = {
                "status_code" : 6001,
                "data": {
                    "message": "Invalid login credentials or not allowed"
                },
            }
    else:
        response_data = {
            "status_code" : 6001,
            "data": {
                "message": "Invalid login credentials or not allowed"
            },
        }

    return Response(response_data)



@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def category(request):
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



@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def category_add(request):
    user=request.user

    serializer = AddCategorySerializer(data=request.data)

    if serializer.is_valid():
        if user.is_manager:
            serializer.save()

            response_data = {
                "staus_code": 6000,
                "data": serializer.data,
                "status":"Category Created."
            }

        else:
            response_data = {
                "staus_code": 6001,
                "data": serializer.data,
                "status":"Unauthorized Access."
            }

    else:
        response_data = {
            "staus_code": 6001,
            "data": serializer.data,
            "status":"Error Occured."
        }

    return Response(response_data)



@api_view(["PUT"])
@permission_classes ([IsAuthenticated])
def category_edit(request, pk):
    user=request.user


    instance = Category.objects.get(pk=pk)
    serializer = AddCategorySerializer(instance=instance,data=request.data)

    if serializer.is_valid():
        if user.is_manager:

            serializer.save()

            response_data = {
                "staus_code": 6000,
                "data": serializer.data,
                "status":"Category Created."
            }
        else:
            response_data = {
                "staus_code": 6001,
                "data": serializer.data,
                "status":"Unauthorized Access."
            }

    else:
        response_data = {
            "staus_code": 6001,
            "data": serializer.data,
            "status":"Error Occured."
        }

    return Response(response_data)



@api_view(["PUT"])
@permission_classes ([IsAuthenticated])
def category_delete(request, pk):
    user=request.user
    instance = Category.objects.get(pk=pk)
    if user.is_manager:

        instance.delete()

        response_data = {
            "staus_code": 6000,
            "data": "Category deleted.",
            "status":"Category deleted."
        }
    else:
        response_data = {
            "staus_code": 6001,
            "data": "Category Not Deleted.",
            "status":"Unauthorized Access"
        }

    return Response(response_data)


@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def item(request):
    instances = Item.objects.all()
    context = {
        "request": request
    }
    serializer = ItemSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": serializer.data,
    }
    return Response(response_data)


@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def item_add(request):
    user=request.user

    serializer = ItemAddSerializer(data=request.data)

    if serializer.is_valid():
        if user.is_manager:
            serializer.save()

            response_data = {
                "staus_code": 6000,
                "data": serializer.data,
                "status":"Category Created."
            }

        else:
            response_data = {
                "staus_code": 6001,
                "data": serializer.data,
                "status":"Unauthorized Access."
            }

    else:
        response_data = {
            "staus_code": 6001,
            "data": serializer.data,
            "status":"Error Occured."
        }

    return Response(response_data)


@api_view(["PUT"])
@permission_classes ([IsAuthenticated])
def item_edit(request, pk):
    user=request.user


    instance = Item.objects.get(pk=pk)
    serializer = ItemAddSerializer(instance=instance,data=request.data)

    if serializer.is_valid():
        if user.is_manager:

            serializer.save()

            response_data = {
                "staus_code": 6000,
                "data": serializer.data,
                "status":"Category Created."
            }
        else:
            response_data = {
                "staus_code": 6001,
                "data": serializer.data,
                "status":"Unauthorized Access."
            }

    else:
        response_data = {
            "staus_code": 6001,
            "data": serializer.data,
            "status":"Error Occured."
        }

    return Response(response_data)


@api_view(["PUT"])
@permission_classes ([IsAuthenticated])
def item_delete(request, pk):
    user=request.user
    instance = Item.objects.get(pk=pk)
    if user.is_manager:

        instance.delete()

        response_data = {
            "staus_code": 6000,
            "data": "Category deleted.",
            "status":"Category deleted."
        }
    else:
        response_data = {
            "staus_code": 6001,
            "data": "Category Not Deleted.",
            "status":"Unauthorized Access"
        }

    return Response(response_data)


@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def franchise(request):
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



@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def franchise_add(request):
    user=request.user

    serializer = FranchiseAddSerializer(data=request.data)

    if serializer.is_valid():
        if user.is_manager:
            serializer.save()

            response_data = {
                "staus_code": 6000,
                "data": serializer.data,
                "status":"Franchise Created."
            }

        else:
            response_data = {
                "staus_code": 6001,
                "data": serializer.data,
                "status":"Unauthorized Access."
            }

    else:
        response_data = {
            "staus_code": 6001,
            "data": serializer.data,
            "status":"Error Occured."
        }

    return Response(response_data)


@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def franchise_edit(request,pk):
    user=request.user


    instance = Franchise.objects.get(pk=pk)
    serializer = FranchiseSerializer(instance=instance,data=request.data)

    if serializer.is_valid():
        if user.is_manager:

            serializer.save()

            response_data = {
                "staus_code": 6000,
                "data": serializer.data,
                "status":"Category Created."
            }
        else:
            response_data = {
                "staus_code": 6001,
                "data": serializer.data,
                "status":"Unauthorized Access."
            }

    else:
        response_data = {
            "staus_code": 6001,
            "data": serializer.data,
            "status":"Error Occured."
        }

    return Response(response_data)


@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def franchise_delete(request,pk):
    user=request.user
    instance = Franchise.objects.get(pk=pk)
    if user.is_manager:

        instance.delete()

        response_data = {
            "staus_code": 6000,
            "data": "Franchise User deleted.",
            "status":"Franchise User deleted."
        }
    else:
        response_data = {
            "staus_code": 6001,
            "data": "Franchise User Not Deleted.",
            "status":"Unauthorized Access"
        }

    return Response(response_data)


@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def franchise_user(request):
    instances = FranchiseUser.objects.all()
    context = {
        "request": request
    }
    serializer = FranchiseUserSerializer(instances, many=True,context=context)

    response_data = {
        "staus_code": 6000,
        "data": serializer.data,
    }
    return Response(response_data)



@api_view(["POST"])
@permission_classes ([IsAuthenticated])
def franchise_user_add(request):
    user=request.user

    first_name = request.data['first_name']
    phone_number = request.data['phone_number']
    email = request.data['email']
    password = request.data['password']
    franchise = request.data['franchise']

    if not User.objects.filter(phone_number=phone_number).exists():
        if user.is_manager:
            
            fuser = User.objects.create_user(
                first_name=first_name,
                phone_number=phone_number,
                email=email,
                password=password,
                is_franchise=True,
            )

            franchise_user = FranchiseUser.objects.create(
                user=fuser,
                franchise=franchise,
            )

            franchise_user.save()
            fuser.save()

            response_data = {
                "staus_code": 6000,
                "message": "Franchise User Created",
                "status":"Franchise User Created."
            }

        else:
            response_data = {
                "staus_code": 6001,
                "message": "Unable to create",
                "status":"Unauthorized Access."
            }

    else:
        response_data = {
            "staus_code": 6001,
            "message": "Phone Number Already Exists",
            "status":"Error Occured."
        }

    return Response(response_data)



@api_view(["GET"])
@permission_classes ([IsAuthenticated])
def franchise_user_edit(request,id):
    pass


@api_view(["PUT"])
@permission_classes ([IsAuthenticated])
def franchise_user_delete(request, pk):
    user=request.user
    instance = FranchiseUser.objects.get(pk=pk)
    if user.is_manager:

        instance.delete()

        response_data = {
            "staus_code": 6000,
            "data": "Franchise User deleted.",
            "status":"Franchise User deleted."
        }
    else:
        response_data = {
            "staus_code": 6001,
            "data": "Franchise User Not Deleted.",
            "status":"Unauthorized Access"
        }

    return Response(response_data)