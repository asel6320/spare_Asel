from admin_panel.form import PriceUpdateForm
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.db.models import Q
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from part.models import Part
from part.views import BasePartView


@method_decorator(staff_member_required, name="dispatch")
class UpdatePricesView(BasePartView):
    paginate_by = 10
    context_object_name = "parts"
    template_name = "admin/set_new_price.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        search_value = self.request.GET.get("search", "")

        return queryset.filter(
            Q(name__icontains=search_value) | Q(latest_price__icontains=search_value)
        ).order_by("-category")

    def post(self, request):
        form = PriceUpdateForm(request.POST)
        selected_parts = request.POST.getlist("selected_parts")

        if form.is_valid() and selected_parts:
            change_type = request.POST.get("change_type")
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
            request,
            self.template_name,
            {"form": form, "parts": parts, "selected_parts": selected_parts},
        )

    @staticmethod
    def get_parts():
        return Part.objects.order_by("-category")

    @staticmethod
    def update_part_prices(selected_parts, new_price):
        with transaction.atomic():
            for part_id in selected_parts:
                part = Part.objects.get(id=part_id)
                last_price_history = part.price_history.last()
                if last_price_history:
                    last_price_history.price = new_price
                    last_price_history.save()
                else:
                    part.price_history.create(price=new_price)

    @staticmethod
    def update_part_percentage(selected_parts, percentage):
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

    @staticmethod
    def update_part_to(selected_parts, change_to):
        with transaction.atomic():
            for part_id in selected_parts:
                part = Part.objects.get(id=part_id)
                last_price_history = part.price_history.last()
                if last_price_history:
                    last_price_history.price += change_to
                    last_price_history.save()
                else:
                    part.price_history.create(price=change_to)
