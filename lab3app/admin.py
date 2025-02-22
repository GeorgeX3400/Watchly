from django.contrib import admin
from django.contrib.auth.models import Group
from .models import *
# Register your models here.





class BrandAdmin(admin.ModelAdmin):
    list_display = ('country', 'name')
    search_fields = ('name',)

class WatchAdmin(admin.ModelAdmin):
    list_filter = ('brand',)
    search_fields = ('name',)
    fieldsets = (
        ('Model' ,{
            'fields': ('brand', 'name')
        }),
        ('Specs', {
            'fields': ('price', 'water_resistance', 'description', 'movement_type', 'warranty', ),
            'classes': ('collapse',)
        })
    )

class MovementTypeAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class WarrantyAdmin(admin.ModelAdmin):
    search_fields = ('duration_years',)

class MaterialAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class FeatureAdmin(admin.ModelAdmin):
    search_fields = ('name',)

class WatchMaterialAdmin(admin.ModelAdmin):
    search_fields = ('watch',)

class WatchFeatureAdmin(admin.ModelAdmin):
    search_fields = ('watch',)

class CustomUserAdmin(admin.ModelAdmin):
    search_fields = ('username',)

admin.site.register(Watch, WatchAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(MovementType, MovementTypeAdmin)
admin.site.register(Warranty, WarrantyAdmin)
admin.site.register(Material, MaterialAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(WatchMaterial, WatchMaterialAdmin)
admin.site.register(WatchFeature, WatchFeatureAdmin)
admin.site.register(CustomUser, CustomUserAdmin)


# GROUP/USER PERMISSION HANDLING:

admins = Group.objects.get(name="Administratori_produse")

not_admin = CustomUser.objects.get(username="Georgeee")
not_admin.groups.remove(admins)
not_admin = CustomUser.objects.get(username="abcd")
not_admin.groups.remove(admins)

