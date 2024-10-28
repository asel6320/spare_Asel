from django.urls import path
from django.conf.urls.i18n import set_language

app_name = "lang"

urlpatterns = [
    path("set_language/", set_language, name="set_language"),
]
