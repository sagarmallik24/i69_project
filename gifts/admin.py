from django.contrib import admin
from .models import Giftpurchase, GiftPurchaseMessageText, RealGift, VirtualGift, AllGifts
from django.contrib.admin.options import ModelAdmin
# Register your models here.


# admin.site.register(Gift)

@admin.register(Giftpurchase)
class GiftpurchaseAdmin(ModelAdmin):
    list_display = ['user', 'purchased_on', 'receiver','gift']
    search_fields = ['user__username', 'user__email', 'user__fullName', 'receiver__username','receiver__email', 'receiver__fullName', 'gift__type']
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(GiftpurchaseAdmin, self).changelist_view(request, extra_context)

class VirtualGiftAdmin(ModelAdmin):
    list_display = ['gift_name', 'cost',]
    search_fields = ['gift_name', 'cost',  'allgift__type']
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(VirtualGiftAdmin, self).changelist_view(request, extra_context)
    
class AllGiftsAdmin(ModelAdmin):
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(AllGiftsAdmin, self).changelist_view(request, extra_context)
   
    
class RealGiftAdmin(ModelAdmin):
    list_display = ['gift_name', 'cost',]
    search_fields = ['gift_name', 'cost', 'allgift__type']
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(RealGiftAdmin, self).changelist_view(request, extra_context)
   

admin.site.register(GiftPurchaseMessageText)
admin.site.register(AllGifts, AllGiftsAdmin)
admin.site.register(RealGift, RealGiftAdmin)
admin.site.register(VirtualGift,VirtualGiftAdmin)
