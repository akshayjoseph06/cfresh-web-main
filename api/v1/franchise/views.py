from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate




@api_view(["POST"])
@permission_classes ([AllowAny])
def login(request):

    username=request.POST.get('username')
    password=request.POST.get('password')

    if username and password:
        user = authenticate(request, username=username, password=password)

        if user.is_franchise:
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

