from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q, Subquery, OuterRef, DecimalField
from django.shortcuts import render
from django.utils.http import urlencode
from webapp.models.price_history import PriceHistory
from django.views.generic import ListView, DetailView

from webapp.forms import SearchForm, PartsFilterForm
from webapp.models import Part, Country, CarBrand, CarModel, Category, PriceHistory


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
        return None

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # No search form in this view, so we exclude 'search_form'
        context.pop('search_form', None)
        return context


class PartsMainView(ListView):
    model = Part
    template_name = 'part/parts_main.html'
    context_object_name = 'parts'
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_filter_form(self):
        return PartsFilterForm(self.request.GET)

    def get_search_value(self):
        form = self.form
        if form.is_valid():
            return form.cleaned_data['search']

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_queryset(self):
        queryset = super().get_queryset()

        latest_price = Subquery(
            PriceHistory.objects.filter(part=OuterRef('pk')).order_by('-date_changed').values('price')[:1],
            output_field=DecimalField()
        )
        queryset = queryset.annotate(latest_price=latest_price)

        form = self.get_filter_form()
        if form.is_valid():
            country = form.cleaned_data.get('country')
            brand = form.cleaned_data.get('brand')
            model = form.cleaned_data.get('model')
            part_type = form.cleaned_data.get('part_type')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')

            if country:
                queryset = queryset.filter(vehicle_info__countries=country)
            if brand:
                queryset = queryset.filter(vehicle_info__model__brand=brand)
            if model:
                queryset = queryset.filter(vehicle_info__model=model)
            if part_type:
                queryset = queryset.filter(category=part_type)
            if min_price:
                queryset = queryset.filter(latest_price__gte=min_price)
            if max_price:
                queryset = queryset.filter(latest_price__lte=max_price)

        if self.search_value:
            queryset = queryset.filter(
                Q(name__icontains=self.search_value) | Q(latest_price__icontains=self.search_value)
            )

        return queryset.order_by('-latest_price')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        context['filter_form'] = self.get_filter_form()
        context['countries'] = Country.objects.all()
        context['brands'] = CarBrand.objects.all()
        context['models'] = CarModel.objects.all()
        context['categories'] = Category.objects.all()
        if self.search_value:
            context["search"] = urlencode({"search": self.search_value})
            context["search_value"] = self.search_value
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


def get_models(request):
    brand_id = request.GET.get('brand_id')
    models = CarModel.objects.filter(brand_id=brand_id).values('id', 'name')
    return JsonResponse({'models': list(models)})
