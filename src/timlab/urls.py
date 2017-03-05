# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import url
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^p/', include('projects.urls')),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
