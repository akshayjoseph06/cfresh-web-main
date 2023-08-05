from django.urls import path

from franchise import views


app_name = "franchise"

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('account/', views.account, name="account"),

    path('items/', views.items, name="items"),
    path('variants/', views.variants, name="variants"),
]