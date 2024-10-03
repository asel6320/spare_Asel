from django.contrib import admin
from django.shortcuts import render
from django.urls import path

from webapp.models.category import Category
from webapp.models.part import Part
from webapp.models.car import CarModel, CarBrand
from webapp.models.engine import Engine
from webapp.models.country import Country
from webapp.models.vehicleinfo import VehicleInfo
from webapp.models import Review, Order


admin.site.register(Category)
admin.site.register(CarBrand)
admin.site.register(Engine)
admin.site.register(Country)

class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'vehicle_info', 'amount')
    list_filter = ('category', 'vehicle_info__model__brand', 'amount')

admin.site.register(Part, PartAdmin)


class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'year_of_manufacture')
    list_filter = ('brand', 'year_of_manufacture')

admin.site.register(CarModel, CarModelAdmin)


class VehicleInfoAdmin(admin.ModelAdmin):
    list_display = ('vehicle_type', 'model', 'year_of_manufacture', 'engine')
    list_filter = ('vehicle_type', 'year_of_manufacture', 'engine')

admin.site.register(VehicleInfo, VehicleInfoAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('part', 'user', 'text')
    list_filter = ('part', 'user')

admin.site.register(Review, ReviewAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'created_at')
    list_filter = ('user', 'created_at')

admin.site.register(Order, OrderAdmin)



