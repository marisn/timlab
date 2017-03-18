# -*- coding: utf-8 -*-
from django.contrib import admin

from images.models import Image, ImageLabel


class ImageAdmin(admin.ModelAdmin):
    list_display = ('filename', 'project', 'updated', )
    readonly_fields = ('preview',)


class ImageLabelAdmin(admin.ModelAdmin):
    list_display = ('image', 'user', 'updated', 'label', 'project',)


admin.site.register(Image, ImageAdmin)
admin.site.register(ImageLabel, ImageLabelAdmin)
