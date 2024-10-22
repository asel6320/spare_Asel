# from django.contrib import admin as admin_panel
# from orders.models import Order, OrderPart
# from part.models import Part
# from webapp.models import Review
# from webapp.models.car import CarModel, CarBrand
# from webapp.models.category import Category
# from webapp.models.country import Country
# from webapp.models.engine import Engine
# from webapp.models.news import News
# from webapp.models.vehicleinfo import VehicleInfo
#
# admin_panel.site.register(Category)
# admin_panel.site.register(CarBrand)
# admin_panel.site.register(Engine)
# admin_panel.site.register(Country)
#
#
# class PartAdmin(admin_panel.ModelAdmin):
#     list_display = ('name', 'category', 'vehicle_info', 'amount')
#     list_filter = ('category', 'vehicle_info__model__brand', 'amount')
#
#
# admin_panel.site.register(Part, PartAdmin)
#
#
# class CarModelAdmin(admin_panel.ModelAdmin):
#     list_display = ('name', 'brand', 'year_of_manufacture')
#     list_filter = ('brand', 'year_of_manufacture')
#
#
# admin_panel.site.register(CarModel, CarModelAdmin)
#
#
# class VehicleInfoAdmin(admin_panel.ModelAdmin):
#     list_display = ('vehicle_type', 'model', 'year_of_manufacture', 'engine')
#     list_filter = ('vehicle_type', 'year_of_manufacture', 'engine')
#
#
# admin_panel.site.register(VehicleInfo, VehicleInfoAdmin)
#
#
# class ReviewAdmin(admin_panel.ModelAdmin):
#     list_display = ('part', 'user', 'text')
#     list_filter = ('part', 'user')
#
#
# admin_panel.site.register(Review, ReviewAdmin)
#
#
# class OrderAdmin(admin_panel.ModelAdmin):
#     list_display = ('user', 'first_name', 'last_name', 'created_at')
#     list_filter = ('user', 'created_at')
#
#
# admin_panel.site.register(Order, OrderAdmin)
#
#
# class OrderPartAdmin(admin_panel.ModelAdmin):
#     list_display = ('id', 'get_customer', 'get_number', 'get_part', 'quantity')
#     list_filter = ('order__user__first_name', 'order__user__last_name', 'part__name')
#     search_fields = ('order__user__first_name', 'order__user__last_name', 'part__name')
#
#     def get_customer(self, obj):
#         return f"{obj.order.last_name} {obj.order.first_name}"
#
#     get_customer.short_description = "ФИО"
#
#     def get_number(self, obj):
#         return f"{obj.order.phone}"
#
#     get_number.short_description = "Телефон"
#
#     def get_part(self, obj):
#         return obj.part.name
#
#     get_part.short_description = 'Товар'
#
#
# admin_panel.site.register(OrderPart, OrderPartAdmin)
#
#
# class NewsAdmin(admin_panel.ModelAdmin):
#     list_display = ('title', 'short_description', 'full_text', 'published_at')
#     list_filter = ('title', 'short_description', 'published_at')
#     search_fields = ('title', 'short_description', 'full_text')
#
#
# admin_panel.site.register(News, NewsAdmin)
