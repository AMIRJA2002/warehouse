from django.contrib import admin
from . import models


@admin.register(models.Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'address', 'type')


@admin.register(models.Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'name', 'type', 'number_of_products', 'section_capacity')


@admin.register(models.Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'section', 'is_enable', 'mac_address', 'end_rent_charge')
