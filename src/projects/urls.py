# -*- coding: utf-8 -*-
from django.conf.urls import url

from projects.views import ProjectsListView, ProjectDetailView
from images.views import ImageLabelUpdateView

urlpatterns = [
    url(r'^$', ProjectsListView.as_view(), name='projects-list'),
    url(r'^(?P<slug>[-\w]+)/?$', ProjectDetailView.as_view(), name='porject-detail'),
    url(r'^[-\w]+/image/(?P<pk>[0-9]+)/?$', ImageLabelUpdateView.as_view(), name='image-label-update'),
]
