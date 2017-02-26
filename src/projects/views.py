# -*- coding: utf-8 -*-
from django.views.generic.list import ListView

from projects.models import Project


class ProjectsListView(ListView):
    model = Project
    order = ('is_active', 'created')
