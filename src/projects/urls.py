# -*- coding: utf-8 -*-
from django.conf.urls import url

from projects.views import ProjectsListView, ProjectDetailView

urlpatterns = [
    url(r'^$', ProjectsListView.as_view(), name='projects-list'),
    url(r'^(?P<slug>[-\w]+)/?$', ProjectDetailView.as_view(), name='porject-detail'),
]
