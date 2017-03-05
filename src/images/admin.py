# -*- coding: utf-8 -*-
from django.contrib import admin

from images.models import Image, ImageLabel

admin.site.register(Image)
admin.site.register(ImageLabel)
