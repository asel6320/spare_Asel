from django.contrib import admin
from webapp.models.category import Category
from webapp.models.part import Part
from webapp.models.user import User
from webapp.models.car import CarModel, CarBrand
from webapp.models.engine import Engine
from webapp.models.country import Country
from webapp.models.vehicleinfo import VehicleInfo


admin.site.register(Category)
admin.site.register(Part)
admin.site.register(User)
admin.site.register(CarModel)
admin.site.register(CarBrand)
admin.site.register(Engine)
admin.site.register(Country)
admin.site.register(VehicleInfo)