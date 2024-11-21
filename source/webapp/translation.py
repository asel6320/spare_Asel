from modeltranslation.translator import register, TranslationOptions
from webapp.models import CarBrand, CarModel, Category, VehicleInfo

@register(CarBrand)
class CarBrandTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(CarModel)
class CarModelTranslationOptions(TranslationOptions):
    fields = ('name',)

@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description')

@register(VehicleInfo)
class VehicleInfoTranslationOptions(TranslationOptions):
    fields = ('body_type',)