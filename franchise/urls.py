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

    path('flash-sales/', views.flashsale, name="flashsale"),
    path('flash-sales/delete/<int:id>/', views.flashsale_delete, name="flashsale_delete"),
    path('flash-sales/add/<int:id>/', views.flashsale_add, name="flashsale_add"),

    path('todays-deals/', views.todaysdeal, name="todaysdeal"),
    path('todays-deals/delete/<int:id>/', views.todaysdeal_delete, name="todaysdeal_delete"),
    path('todays-deals/add/<int:id>/', views.todaysdeal_add, name="todaysdeal_add"),

    path('banners/', views.banners, name="banners"),
    path('banners/delete/<int:id>/', views.banners_delete, name="banners_delete"),
    path('banners/add/<str:type>/', views.banners_add, name="banners_add"),

    path('posters/', views.posters, name="posters"),
    path('posters/delete/<int:id>/', views.posters_delete, name="posters_delete"),
    path('posters/add/<str:type>/', views.posters_add, name="posters_add"),

    path('static/', views.static, name="static"),
    path('static/delete/<int:id>/', views.static_delete, name="static_delete"),
    path('static/add/<str:type>/', views.static_add, name="static_add"),

]