from django.contrib import admin

from .models import Customer, CustomerAddress, Cart


admin.site.register(Customer)
admin.site.register(CustomerAddress)
admin.site.register(Cart)

