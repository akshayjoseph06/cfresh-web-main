from django.contrib import admin

from .models import Category, Item, VariantDetail, FranchiseItem

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(VariantDetail)
admin.site.register(FranchiseItem)
