from django.urls import path

from contacts.views import contact_request

app_name = "contacts"


urlpatterns = [
    path("contact/", contact_request, name="contact"),
]
