from django.contrib import admin
from .models import Category, Country, Tea, Equipment, Kit

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category_id',
        'category',
        'created',
        'updated',
    )


class CountryAdmin(admin.ModelAdmin):
    list_display = (
        'country_id',
        'country',
        'created',
        'updated',
    )


class TeaAdmin(admin.ModelAdmin):
    list_display = (
        'product_id',
        'internal_name',
        'product_name',
        'weight',
        'category',
        'price',
        'created',
        'updated',
    )


class EquipmentAdmin(admin.ModelAdmin):
    list_display = (
        'product_id',
        'internal_name',
        'product_name',
        'category',
        'price',
        'created',
        'updated',
    )


class KitAdmin(admin.ModelAdmin):
    list_display = (
        'product_id',
        'internal_name',
        'product_name',
        'category',
        'price',
        'created',
        'updated',
    )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(Tea, TeaAdmin)
admin.site.register(Equipment, EquipmentAdmin)
admin.site.register(Kit, KitAdmin)
