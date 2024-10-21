from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django.apps import apps
from django.forms import modelform_factory
import sys


sys.stdout.reconfigure(encoding='utf-8')

EXCLUDED_APPS = {'auth', 'contenttypes', 'admin', 'sessions'}

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
        'order': 'orders.Order',
        'orderpart': 'orders.OrderPart',
        'review': 'webapp.Review',
        'news': 'webapp.News',
    }

    print(f'Запрос модели: {model_name}')  # Отладка

    if model_name not in app_model_mapping:
        print(f'Ошибка: Модель "{model_name}" не найдена в маппинге.')
        raise Http404('Модель не найдена в конфигурации.')

    try:
        model_path = app_model_mapping[model_name]
        print(f'Ищем модель по пути: {model_path}')  # Отладка
        return apps.get_model(model_path)
    except LookupError:
        print(f'Ошибка: Модель {model_path} не найдена.')  # Отладка
        raise Http404(f'Модель {model_name} не найдена.')

@staff_required
def admin_home(request):
    models = [
        model for model in apps.get_models()
        if model._meta.app_label not in EXCLUDED_APPS
    ]

    models_data = [
        {
            'model_name': model._meta.model_name,
            'verbose_name_plural': model._meta.verbose_name_plural,
        }
        for model in models
    ]

    return render(request, 'home.html', {'models': models_data})

@staff_required
def model_list(request, model_name):
    print(f'Получение списка для модели: {model_name}')  # Отладка
    model = get_model_or_404(model_name)
    objects = model.objects.all()

    print(f'Найдено {objects.count()} объектов для модели {model_name}.')  # Отладка

    if not objects.exists():
        print(f'Предупреждение: В модели {model_name} нет объектов.')  # Отладка

    return render(request, 'model_list.html', {'objects': objects, 'model_name': model_name})


@staff_required
def model_add(request, model_name):
    """Добавление нового объекта в модель."""
    model = get_model_or_404(model_name)
    if request.method == 'POST':
        form = get_model_form(model)(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Запись добавлена в {model_name}')
            return redirect('admin_panel:model_list', model_name=model_name)
    else:
        form = get_model_form(model)()
    return render(request, 'model_form.html', {'form': form, 'model_name': model_name})


@staff_required
def model_edit(request, model_name, pk):
    """Редактирование существующего объекта модели."""
    model = get_model_or_404(model_name)
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        form = get_model_form(model)(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, f'Запись в {model_name} обновлена')
            return redirect('admin_panel:model_list', model_name=model_name)
    else:
        form = get_model_form(model)(instance=obj)
    return render(request, 'model_form.html', {'form': form, 'model_name': model_name})


@staff_required
def model_delete(request, model_name, pk):
    """Удаление объекта модели."""
    model = get_model_or_404(model_name)
    obj = get_object_or_404(model, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, f'Запись из {model_name} удалена')
        return redirect('admin_panel:model_list', model_name=model_name)
    return render(request, 'model_delete.html', {'obj': obj, 'model_name': model_name})


def get_model_form(model):
    """Генерация формы для модели."""
    return modelform_factory(model, fields='__all__')
