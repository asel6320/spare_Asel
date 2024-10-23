from django.contrib import admin
from django.contrib import messages
from django.db import transaction
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.utils.translation import ngettext
from webapp.models import PriceHistory
from .form import PriceUpdateForm


class UpdatePricesActionMixin:

    @admin.action(description='Массовая смена цен')
    def update_prices(self, request, queryset):
        if 'apply' in request.POST:
            form = self._get_price_form(request)

            if form.is_valid():
                self._apply_price_update(form, queryset, request)
                return HttpResponseRedirect(request.get_full_path())
            else:
                return self._render_price_form(request, form, queryset)
        else:
            form = PriceUpdateForm()
            return self._render_price_form(request, form, queryset)

    def _get_price_form(self, request):
        return PriceUpdateForm(request.POST)

    def _apply_price_update(self, form, queryset, request):

        price = form.cleaned_data.get('price')
        int(price)
        updated_count = 0
        with transaction.atomic():
            for part in queryset:
                part.price = price
                part.save()
                updated_count += 1
        self._send_success_message(request, updated_count)

    def _send_success_message(self, request, updated_count):
        message = ngettext(
            "%d цена была успешно изменена.",
            "%d цены были успешно изменены.",
            updated_count,
        ) % updated_count

        self.message_user(request, message, messages.SUCCESS)

    def _render_price_form(self, request, form, queryset):
        context = {
            'form': form,
            'queryset': queryset,
        }
        return TemplateResponse(request, 'admin/set_new_price.html', context)


class PriceHistoryAdmin(admin.ModelAdmin, UpdatePricesActionMixin):
    list_display = ['price', 'date_changed']
    ordering = ['-price']
    actions = [UpdatePricesActionMixin.update_prices]


admin.site.register(PriceHistory, PriceHistoryAdmin)
