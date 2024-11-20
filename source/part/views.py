from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import DecimalField, OuterRef, Q, Subquery
from django.utils.http import urlencode
from django.views.generic import DetailView, ListView
from documents.models import PartDocument
from favorite.models import Favorite
from part.form import PartsFilterForm
from part.models import Part
from webapp.forms import SearchForm
from webapp.forms.review_form import ReviewForm
from webapp.models import CarBrand, CarModel, Category, Country, PriceHistory
from webapp.models.news import News
from webapp.models.review import Review


class BasePartView(ListView):
    model = Part

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        form = self.form
        if form.is_valid():
            return form.cleaned_data["search"]
        return None

    def get_queryset(self):
        queryset = super().get_queryset()

        latest_price = Subquery(
            PriceHistory.objects.filter(part=OuterRef("pk"))
            .order_by("-date_changed")
            .values("price")[:1],
            output_field=DecimalField(),
        )

        queryset = queryset.annotate(latest_price=latest_price)

        if self.search_value:
            queryset = queryset.filter(
                Q(name__icontains=self.search_value)
                | Q(latest_price__icontains=self.search_value)
            )

        queryset = queryset.order_by("-latest_price")

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
    context_object_name = "parts"
    template_name = "index.html"
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest"] = News.objects.order_by("-published_at")[:5]
        context.pop("search_form", None)
        favorites = (
            Favorite.objects.filter(user=self.request.user)
            if self.request.user.is_authenticated
            else Favorite.objects.filter(session_key=self.request.session.session_key)
        )
        context["favorites"] = favorites.values_list("part_id", flat=True)
        return context


class PartsMainView(ListView):
    model = Part
    template_name = "part/parts_main.html"
    context_object_name = "parts"
    paginate_by = 12

    def dispatch(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().dispatch(request, *args, **kwargs)

    def get_search_value(self):
        form = self.form
        if form.is_valid():
            return form.cleaned_data["search"]
        return None

    def get_form(self):
        return SearchForm(self.request.GET)

    def get_queryset(self):
        queryset = super().get_queryset()

        latest_price = Subquery(
            PriceHistory.objects.filter(part=OuterRef("pk"))
            .order_by("-date_changed")
            .values("price")[:1],
            output_field=DecimalField(),
        )
        queryset = queryset.annotate(latest_price=latest_price)

        if self.search_value:
            queryset = queryset.filter(
                Q(name__icontains=self.search_value)
                | Q(latest_price__icontains=self.search_value)
            )

        form = self.get_filter_form()
        if form.is_valid():
            country = form.cleaned_data.get("country")
            brand = form.cleaned_data.get("brand")
            model = form.cleaned_data.get("model")
            category = form.cleaned_data.get("category")
            min_price = form.cleaned_data.get("min_price")
            max_price = form.cleaned_data.get("max_price")

            if country:
                queryset = queryset.filter(vehicle_info__countries=country)
            if brand:
                queryset = queryset.filter(vehicle_info__model__brand=brand)
            if model:
                queryset = queryset.filter(vehicle_info__model=model)
            if category:
                queryset = queryset.filter(category=category)
            if min_price:
                queryset = queryset.filter(latest_price__gte=min_price)
            if max_price:
                queryset = queryset.filter(latest_price__lte=max_price)

                # Обработка сортировки
            order_by = self.request.GET.get("order_by")
            if order_by == "price":
                queryset = queryset.order_by("latest_price")  # От дешевых к дорогим
            elif order_by == "-price":
                queryset = queryset.order_by("-latest_price")  # От дорогих к дешевым
            else:
                queryset = queryset.order_by("-latest_price")  # По умолчанию

            return queryset

    def get_filter_form(self):
        return PartsFilterForm(self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["search_form"] = self.form
        context["filter_form"] = self.get_filter_form()
        context["countries"] = Country.objects.all()
        context["brands"] = CarBrand.objects.all()
        context["models"] = CarModel.objects.all()
        context["categories"] = Category.objects.all()
        context["reviews"] = Review.objects.all()
        if self.search_value:
            context["search"] = urlencode({"search": self.search_value})
            context["search_value"] = self.search_value
        return context


class PartsDetailView(DetailView):
    model = Part
    context_object_name = "part"
    template_name = "part/parts_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        part_category = self.object.category
        related_parts = Part.objects.filter(category=part_category).exclude(
            pk=self.object.pk
        )[:5]
        context["related_parts"] = related_parts
        context["category"] = part_category
        context["reviews"] = Review.objects.filter(part=self.object).select_related('user')
        context["documents"] = PartDocument.objects.filter(part=self.object)

        favorites = (
            Favorite.objects.filter(user=self.request.user)
            if self.request.user.is_authenticated
            else Favorite.objects.filter(session_key=self.request.session.session_key)
        )
        context["favorites"] = favorites.values_list("part_id", flat=True)
        context["review_form"] = ReviewForm()

        return context

    def post(self, request, *args, **kwargs):
        part = self.get_object()
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.part = part
            review.user = request.user
            review.save()
            messages.success(request, f'Вы успешно оставили отзыв к запчасти: {review.part}')
            return redirect('part:part_detail', pk=part.pk)
        return self.get(request, *args, **kwargs)