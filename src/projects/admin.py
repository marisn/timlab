# -*- coding: utf-8 -*-
from django.contrib import admin

from projects.models import Project, Label


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('slug', 'title', 'is_active',)
    list_filter = ('is_active',)


class LabelAdmin(admin.ModelAdmin):
    list_display = ('text', 'code', 'project',)
    list_filter = ('project__slug',)


admin.site.register(Project, ProjectAdmin)
admin.site.register(Label, LabelAdmin)
