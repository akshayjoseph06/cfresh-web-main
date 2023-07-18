from django.contrib import admin

from .models import Category, Item, ItemVariant, VariantDetail, FranchiseItem

admin.site.register(Category)
admin.site.register(Item)
admin.site.register(VariantDetail)
admin.site.register(ItemVariant)
admin.site.register(FranchiseItem)
