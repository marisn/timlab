# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.conf.urls import include
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html')),
    url(r'^p/', include('projects.urls')),
    url(r'^admin/', admin.site.urls)
]
