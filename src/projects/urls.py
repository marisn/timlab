# -*- coding: utf-8 -*-
from django.conf.urls import url

from projects.views import ProjectsListView

urlpatterns = [
    url(r'^$', ProjectsListView.as_view(), name='projects-list'),
]
