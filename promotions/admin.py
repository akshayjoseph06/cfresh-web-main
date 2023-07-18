from django.contrib import admin

from promotions.models import FlashSale, FlashSaleItems, TodayDeal, TodayDealItems, Banner, StaticBanner, Poster, Offer


admin.site.register(FlashSale)
admin.site.register(FlashSaleItems)
admin.site.register(TodayDeal)
admin.site.register(TodayDealItems)
admin.site.register(StaticBanner)
admin.site.register(Banner)
admin.site.register(Poster)
admin.site.register(Offer)
