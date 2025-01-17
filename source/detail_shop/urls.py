"""
URL configuration for detail_shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls')
"""

from debug_toolbar.toolbar import debug_toolbar_urls
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = (
    [
        path("", include("part.urls")),
        path("admin/", admin.site.urls, name="admin"),
        path("user/", include("webapp.urls")),
        path("cart/", include("carts.urls")),
        path("order/", include("orders.urls")),
        path("accounts/", include("accounts.urls")),
        path("admin_panel/", include("admin_panel.urls")),
        path("lang/", include("lang.urls")),
        path("contacts/", include("contacts.urls")),
        path("crm/", include("crm.urls")),
        path("favorite/", include("favorite.urls")),
        path("newsletter/", include("newsletter.urls")),
        path('summernote/', include('django_summernote.urls')),
    ]
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    + debug_toolbar_urls()
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
)

urlpatterns += i18n_patterns(
    path("", include("django.conf.urls.i18n")),
)
