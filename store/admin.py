from django.contrib import admin
from .models import *
# Register your models here.

def deactivate(modeladmin, request, queryset):
    queryset.update(is_active=False)

def activate(modeladmin, request, queryset):
    queryset.update(is_active=True)

class ProductAdmin(admin.ModelAdmin):
    list_display = ['custom_id', 'name', 'price', 'is_active']
    actions = [deactivate, activate]

class ProductDescriptionAdmin(admin.ModelAdmin):
    list_display = ['singer']

class SingerAdmin(admin.ModelAdmin):
    list_display = ['singer_name']

class LabelAdmin(admin.ModelAdmin):
    list_display = ['label_name']

class FactoryAdmin(admin.ModelAdmin):
    list_display = ['factory_name']
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['album_name', 'singer', 'label']

class TrackAdmin(admin.ModelAdmin):
    list_display = ['track_no','track_name']


admin.site.register(Customer)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductDescription, ProductDescriptionAdmin)
admin.site.register(Singer, SingerAdmin)
admin.site.register(Album, AlbumAdmin)
admin.site.register(Track)
admin.site.register(Factory, FactoryAdmin)
admin.site.register(Label, LabelAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
