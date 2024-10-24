from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from admin_panel.form import PriceUpdateForm
from part.models import Part


@method_decorator(staff_member_required, name='dispatch')
class UpdatePricesView(View):
    def get(self, request):
        form = PriceUpdateForm()
        parts = self.get_parts()
        return render(request, 'admin/set_new_price.html', {'form': form, 'parts': parts})

    def post(self, request):
        form = PriceUpdateForm(request.POST)
        if form.is_valid():
            new_price = form.cleaned_data.get('price')
            selected_parts = request.POST.getlist('selected_parts')

            if not selected_parts:
                messages.error(request, 'Выберите хотя бы одну запчасть для обновления цен')
                return redirect('admin_panel:update_prices')

            self.update_part_prices(selected_parts, new_price)
            messages.success(request, f'Успешно обновлено цен на {len(selected_parts)} запчастей')
            return redirect('admin_panel:admin_home')

        parts = self.get_parts()
        return render(request, 'admin/set_new_price.html', {'form': form, 'parts': parts})

    def get_parts(self):
        return Part.objects.order_by('category')

    def update_part_prices(self, selected_parts, new_price):
        with transaction.atomic():
            for part_id in selected_parts:
                part = Part.objects.get(id=part_id)
                last_price_history = part.price_history.last()
                if last_price_history:
                    last_price_history.price = new_price
                    last_price_history.save()
                else:
                    part.price_history.create(price=new_price)
