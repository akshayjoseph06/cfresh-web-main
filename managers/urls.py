from django.urls import path

from managers import views


app_name = "managers"

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('account/', views.account, name="account"),

    path('categories/', views.categories, name="categories"),
    path('categories/add/', views.categories_add, name="categories_add"),
    path('categories/edit/<int:id>/', views.categories_edit, name="categories_edit"),
    path('categories/delete/<int:id>/', views.categories_delete, name="categories_delete"),

    path('products/', views.products, name="products"),
    path('products/add/', views.products_add, name="products_add"),
    path('products/edit/<int:id>/', views.products_edit, name="products_edit"),
    path('products/delete/<int:id>/', views.products_delete, name="products_delete"),

    path('franchise/', views.franchise, name="franchise"),
    path('franchise/add/', views.franchise_add, name="franchise_add"),
    path('franchise/edit/<int:id>/', views.franchise_edit, name="franchise_edit"),
    path('franchise/delete/<int:id>/', views.franchise_delete, name="franchise_delete"),

    # path('franchise/items/', views.franchise_items, name="franchise_items"),
    # path('franchise/items/add/', views.franchise_items_add, name="franchise_items_add"),
    # path('franchise/items/edit/<int:id>/', views.franchise_items_edit, name="franchise_items_edit"),
    # path('franchise/items/delete/<int:id>/', views.franchise_items_delete, name="franchise_items_delete"),

    # path('variations/', views.variations, name="variations"),
    # path('variations/add/', views.variations_add, name="variations_add"),
    # path('variations/edit/<int:id>/', views.variations_edit, name="variations_edit"),
    # path('variations/delete/<int:id>/', views.variations_delete, name="variations_delete"),

    # path('stocks/', views.stocks, name="stocks"),
    # path('stocks/edit/<int:id>/', views.stocks_edit, name="stocks_edit"),

    # path('time-slots/', views.timeslots, name="timeslots"),
    # path('time-slots/add/', views.timeslots_add, name="timeslots_add"),
    # path('time-slots/edit/<int:id>/', views.timeslots_edit, name="timeslots_edit"),
    # path('time-slots/delete/<int:id>/', views.timeslots_delete, name="timeslots_delete"),

    # path('customers/', views.customers, name="customers"),

    # path('franchise/users/', views.franchise_users, name="franchise_users"),
    # path('franchise/users/add/', views.franchise_users_add, name="franchise_users_add"),
    # path('franchise/users/edit/<int:id>/', views.franchise_users_edit, name="franchise_users_edit"),
    # path('franchise/users/delete/<int:id>/', views.franchise_users_delete, name="franchise_users_delete"),

    # path('delivery-boys/', views.deliveryboys, name="deliveryboys"),
    # path('delivery-boys/add/', views.deliveryboys_add, name="deliveryboys_add"),
    # path('delivery-boys/edit/<int:id>/', views.deliveryboys_edit, name="deliveryboys_edit"),
    # path('delivery-boys/delete/<int:id>/', views.deliveryboys_delete, name="deliveryboys_delete"),

    # path('banners/', views.banners, name="banners"),
    # path('banners/add/', views.banners_add, name="banners_add"),
    # path('banners/edit/<int:id>/', views.banners_edit, name="banners_edit"),
    # path('banners/delete/<int:id>/', views.banners_delete, name="banners_delete"),

    # path('posters/', views.posters, name="posters"),
    # path('posters/add/', views.posters_add, name="posters_add"),
    # path('posters/edit/<int:id>/', views.posters_edit, name="posters_edit"),
    # path('posters/delete/<int:id>/', views.posters_delete, name="posters_delete"),

    # path('static-banners/', views.static, name="static"),
    # path('static-banners/add/', views.static_add, name="static_add"),
    # path('static-banners/edit/<int:id>/', views.static_edit, name="static_edit"),
    # path('static-banners/delete/<int:id>/', views.static_delete, name="static_delete"),

    # path('todays-deals/', views.todaysdeals, name="todaysdeals"),
    # path('todays-deals/add/', views.todaysdeals_add, name="todaysdeals_add"),
    # path('todays-deals/edit/<int:id>/', views.todaysdeals_edit, name="todaysdeals_edit"),
    # path('todays-deals/delete/<int:id>/', views.todaysdeals_delete, name="todaysdeals_delete"),

    # path('flash-sales/', views.flashsales, name="flashsales"),
    # path('flash-sales/add/', views.flashsales_add, name="flashsales_add"),
    # path('flash-sales/edit/<int:id>/', views.flashsales_edit, name="flashsales_edit"),
    # path('flash-sales/delete/<int:id>/', views.flashsales_delete, name="flashsales_delete"),

    # path('offers/', views.offers, name="offers"),
    # path('offers/add/', views.offers_add, name="offers_add"),
    # path('offers/edit/<int:id>/', views.offers_edit, name="offers_edit"),
    # path('offers/delete/<int:id>/', views.offers_delete, name="offers_delete"),
]