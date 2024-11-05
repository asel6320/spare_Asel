import sys
from django.apps import apps
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

sys.stdout.reconfigure(encoding="utf-8")

EXCLUDED_APPS = {"auth", "contenttypes", "admin", "sessions", "orders", "contacts"}


def staff_required(function):
    return user_passes_test(lambda u: u.is_authenticated and u.is_staff)(function)


def get_model_or_404(model_name):
    app_model_mapping = {
        'cart': 'carts.Cart',
        'part': 'part.Part',
        'carbrand': 'webapp.CarBrand',
        'carmodel': 'webapp.CarModel',
        'country': 'webapp.Country',
        'category': 'webapp.Category',
        'engine': 'webapp.Engine',
        'pricehistory': 'webapp.PriceHistory',
        'vehicleinfo': 'webapp.VehicleInfo',
        'user': 'accounts.User',
        'orderpart': 'orders.OrderPart',
        'review': 'webapp.Review',
        'news': 'webapp.News',
        'partdocument': 'documents.PartDocument',
        'favorite': 'webapp.Favorite',
    }

    print(f"Запрос модели: {model_name}")  # Отладка

    if model_name not in app_model_mapping:
        raise Http404('Модель не найдена в конфигурации.')

    try:
        model_path = app_model_mapping[model_name]
        return apps.get_model(model_path)
    except LookupError:
        raise Http404(f'Модель {model_name} не найдена.')


@staff_required
def admin_home(request):
    models = [
        model for model in apps.get_models()
        if model._meta.app_label not in EXCLUDED_APPS
    ]

    models_data = [
        {
            "model_name": model._meta.model_name,
            "verbose_name_plural": model._meta.verbose_name_plural,
        }
        for model in models
    ]

    return render(request, "home.html", {"models": models_data})


@staff_required
def model_list(request, model_name):
    model = get_model_or_404(model_name)
    objects = model.objects.all()

    return render(request, 'model_list.html', {
        'objects': objects,
        'model_name': model_name,
        'verbose_name_plural': model._meta.verbose_name_plural,
    })

@staff_required
def model_add(request, model_name):
    model = get_model_or_404(model_name)
    if request.method == "POST":
        form = get_model_form(model)(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Запись успешно добавлена в {model_name}')
            return redirect('admin_panel:model_list', model_name=model_name)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = get_model_form(model)()

    return render(request, 'model_form.html', {'form': form, 'model_name': model_name})

@staff_required
def model_edit(request, model_name, pk):
    model = get_model_or_404(model_name)
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        form = get_model_form(model)(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f"Запись в {model_name} обновлена")
            return redirect("admin_panel:model_list", model_name=model_name)
    else:
        form = get_model_form(model)(instance=obj)
    return render(request, "model_form.html", {"form": form, "model_name": model_name})


@staff_required
def model_delete(request, model_name, pk):
    model = get_model_or_404(model_name)
    obj = get_object_or_404(model, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, f"Запись из {model_name} удалена")
        return redirect("admin_panel:model_list", model_name=model_name)
    return render(request, "model_delete.html", {"obj": obj, "model_name": model_name})


def get_model_form(model):
    return modelform_factory(model, fields='__all__')
