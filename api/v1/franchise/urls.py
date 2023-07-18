from django.urls import path

from api.v1.franchise import views


urlpatterns = [
    path('login/', views.login),

]