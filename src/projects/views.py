# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from projects.models import Project


class ProjectsListView(ListView):
    model = Project
    order = ('is_active', 'created')


class ProjectDetailView(DetailView):
    model = Project
