from django.shortcuts import get_object_or_404
from django.db.models import Q, Subquery, OuterRef, DecimalField
from django.shortcuts import render
from django.utils.http import urlencode
from webapp.models.price_history import PriceHistory
from django.views.generic import ListView, DetailView

from webapp.forms import SearchForm
from webapp.models import Part, Country


class BasePartView(ListView):
    model = Part
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        form = self.form
        if form.is_valid():
            return form.cleaned_data['search']

    def get_queryset(self):
        queryset = super().get_queryset()

        latest_price = Subquery(
            PriceHistory.objects.filter(part=OuterRef('pk')).order_by('-date_changed').values('price')[:1],
            output_field=DecimalField()
        )

        queryset = queryset.annotate(latest_price=latest_price)

        if self.search_value:
            queryset = queryset.filter(
                Q(name__icontains=self.search_value) | Q(latest_price__icontains=self.search_value)
            )

        queryset = queryset.order_by('-latest_price')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        context["countries"] = Country.objects.all()
        if self.search_value:
            context["search"] = urlencode({"search": self.search_value})
            context["search_value"] = self.search_value
        return context


class PartsListView(BasePartView):
    context_object_name = 'parts'
    template_name = 'part/index.html'


class PartsByCountryView(BasePartView):
    context_object_name = 'parts_by_country'
    template_name = 'part/parts_by_country.html'

    def get_queryset(self):
        country = get_object_or_404(Country, pk=self.kwargs['pk'])
        return Part.objects.filter(vehicle_info__countries=country).order_by('-price_history__price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['country'] = get_object_or_404(Country, pk=self.kwargs['pk'])
        return context


class PartsDetailView(DetailView):
    model = Part
    context_object_name = 'part'
    template_name = 'part/parts_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part_category = self.object.category
        related_parts = Part.objects.filter(category=part_category).exclude(pk=self.object.pk)[
                        :5]  # Получаем похожие запчасти по категории
        context['related_parts'] = related_parts
        context['category'] = part_category

        return context


def about_us(request):
    return render(request, 'part/about_us.html')
