from django.contrib import admin

from .models import FranchiseUser, Franchise, TimeSlot


admin.site.register(Franchise)
admin.site.register(FranchiseUser)
admin.site.register(TimeSlot)
