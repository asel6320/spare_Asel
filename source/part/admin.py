from django.contrib import admin

from part.models import Part


# Register your models here.
class PartAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'vehicle_info', 'amount', 'video_url')
    list_filter = ('category', 'vehicle_info__model__brand', 'amount', 'video_url')


admin.site.register(Part, PartAdmin)
