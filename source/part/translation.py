from modeltranslation.translator import register, TranslationOptions
from part.models import Part

@register(Part)
class PartTranslationOptions(TranslationOptions):
    fields = ('name', 'description')