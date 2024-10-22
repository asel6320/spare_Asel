from django.contrib import admin
from django.db import transaction
from django.template.response import TemplateResponse
from django.contrib import messages
from django.utils.translation import ngettext

from webapp.models import PriceHistory
from .form import PriceUpdateForm


@admin.action(description='Массовая смена цен')
def update_prices(modeladmin, request, queryset):
    if 'apply' in request.POST:
        form = PriceUpdateForm(request.POST)
        if form.is_valid():
            new_price = form.cleaned_data.get('new_price')
            updated_count = 0
            with transaction.atomic():
                for part in queryset:
                    part.price *= new_price
                    part.save()
                    updated_count += 1
            modeladmin.message_user(
                request,
                ngettext(
                    "%d цена была успешно изменена.",
                    "%d цены были успешно изменены.",
                    updated_count,
                ) % updated_count,
                messages.SUCCESS
            )
            return None
    else:
        form = PriceUpdateForm()

    context = dict(
        form=form,
        queryset=queryset,
    )
    return TemplateResponse(request, 'admin/set_new_price.html', context)


update_prices.short_description = "Обновить цены на выбранные запчасти"


class PriceHistoryAdmin(admin.ModelAdmin):
    list_display = ['price', 'date_changed']
    ordering = ['-price']
    actions = [update_prices]


admin.site.register(PriceHistory, PriceHistoryAdmin)
