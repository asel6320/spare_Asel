from django.contrib import admin
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path

from webapp.models.category import Category
from webapp.models.part import Part
from webapp.models.car import CarModel, CarBrand
from webapp.models.engine import Engine
from webapp.models.country import Country
from webapp.models.vehicleinfo import VehicleInfo
from webapp.models import Review, Order, OrderPart
from webapp.models.news import News

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


class OrderPartAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_customer', 'get_number', 'get_part', 'quantity')
    list_filter = ('order__user__first_name', 'order__user__last_name', 'part__name')
    search_fields = ('order__user__first_name', 'order__user__last_name', 'part__name')

    def get_customer(self, obj):
        return f"{obj.order.last_name} {obj.order.first_name}"

    get_customer.short_description = "ФИО"

    def get_number(self, obj):
        return f"{obj.order.phone}"

    get_number.short_description = "Телефон"

    def get_part(self, obj):
        return obj.part.name

    get_part.short_description = 'Товар'


admin.site.register(OrderPart, OrderPartAdmin)


class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'short_description', 'full_text', 'published_at')
    list_filter = ('title', 'short_description', 'published_at')
    search_fields = ('title', 'short_description', 'full_text')

admin.site.register(News, NewsAdmin)