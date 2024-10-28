from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.generic import View
from admin_panel.form import PriceUpdateForm
from part.models import Part


@method_decorator(staff_member_required, name="dispatch")
class UpdatePricesView(View):
    def get(self, request):
        parts = self.get_parts()
        form = PriceUpdateForm()
        return render(
            request, "admin/set_new_price.html", {"form": form, "parts": parts}
        )

    def post(self, request):
        form = PriceUpdateForm(request.POST)
        if form.is_valid():
            change_type = request.POST.get("change_type")
            selected_parts = request.POST.getlist("selected_parts")

            if not selected_parts:
                messages.error(
                    request, "Выберите хотя бы одну запчасть для обновления цен"
                )
                return redirect("admin_panel:update_prices")

            if change_type == "price":
                new_price = form.cleaned_data.get("price")
                self.update_part_prices(selected_parts, new_price)
            elif change_type == "percentage":
                percentage = form.cleaned_data.get("percentage")
                self.update_part_percentage(selected_parts, percentage)
            elif change_type == "price_to":
                change_to = form.cleaned_data.get("price_to")
                self.update_part_to(selected_parts, change_to)

            messages.success(
                request, f"Успешно обновлено цен на {len(selected_parts)} запчастей"
            )
            return redirect("admin_panel:admin_home")

        parts = self.get_parts()
        return render(
            request, "admin/set_new_price.html", {"form": form, "parts": parts}
        )

    def get_parts(self):
        return Part.objects.order_by("-category")

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

    def update_part_percentage(self, selected_parts, percentage):
        with transaction.atomic():
            for part_id in selected_parts:
                part = Part.objects.get(id=part_id)
                last_price_history = part.price_history.last()
                if last_price_history:
                    new_price = last_price_history.price * (1 + percentage / 100)
                    last_price_history.price = new_price
                    last_price_history.save()
                else:
                    part.price_history.create(price=new_price)

    def update_part_to(self, selected_parts, change_to):
        with transaction.atomic():
            for part_id in selected_parts:
                part = Part.objects.get(id=part_id)
                last_price_history = part.price_history.last()
                if last_price_history:
                    last_price_history.price += change_to
                    last_price_history.save()
                else:
                    part.price_history.create(price=change_to)
