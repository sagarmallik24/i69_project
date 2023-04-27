from django.contrib import admin
from django.contrib.admin.options import ModelAdmin

# Register your models here.

from .models import *

from easy_select2 import select2_modelform

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ExportActionMixin


@admin.register(Purchase)
class PurchaseAdmin(ModelAdmin):
    list_display = ['user', 'purchased_on', 'coins', 'method', 'money']
    search_fields = ["user__username", "user__fullName", "user__email"]
    
    class Media:
        js = ("admin/js/admin_paginator.js",)
        
    def changelist_view(self, request, extra_context=None):
        request.GET = request.GET.copy()
        page_param = int(request.GET.pop('list_per_page', [25])[0])
        self.list_per_page = page_param
        return super(PurchaseAdmin, self).changelist_view(request, extra_context)


admin.site.register(Package)
admin.site.register(PackagePurchase)