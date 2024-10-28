from django import template

register = template.Library()


@register.filter
def get_field_value(obj, field_name):
    """Получает значение поля объекта по имени."""
    return getattr(obj, field_name, None)
