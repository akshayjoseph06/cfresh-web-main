from django.urls import path

from api.v1.customer import views


urlpatterns = [
    path('send-otp/', views.otp_send),
    path('verify-otp/', views.otp_verify),
    path('register/', views.register),

    path('franchise/', views.check_franchise),
    path('franchise/update/', views.update_franchise),
    path('franchise/list/', views.list_franchise),

    path('banner/', views.banner),
    path('poster/', views.poster),
    path('static/', views.static),

    path('categories/', views.categories),
   # path('category/<int:id>/', views.category),
    path('products/<int:id>/', views.products),
    # path('product/<int:id>/', views.product),

    path('flash-sale/', views.flash_sale),
    path('todays-deal/', views.todays_deal),

    path('address/', views.address),
    path('address/add/', views.address_add),
    # path('address/edit/<int:id>/', views.address_edit),
    path('address/delete/<int:id>/', views.address_delete),
    path('address/primary/<int:id>/', views.address_primary),

    path('cart/', views.cart),
    path('cart/add/', views.cart_add),
    path('cart/plus/', views.cart_plus),
    path('cart/minus/', views.cart_minus),

    path('time-slot/', views.time_slot),
    path('checkout/', views.checkout),
    path('address/select/', views.address_select),

    path('account/', views.account),

    path('orders/', views.orders),
    path('order/place/', views.place_order),


]