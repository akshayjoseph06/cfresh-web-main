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

    # path('flash-sale/', views.flash_sale),
    # path('todays-deal/', views.todays_deal),

    # path('cart/', views.cart),
    # path('cart/add/<int:id/', views.cart),
    # path('cart/plus/<int:id/', views.cart),
    # path('cart/minus/<int:id/', views.cart),

    # path('time-slot/', views.time_slot),
]