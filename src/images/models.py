# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

from projects.models import Label


class Image(models.Model):
    """
    Reference to a particular image file
    """
    
    filename = models.CharField(max_length=100)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.filename


class ImageLabel(models.Model):
    """
    Link between image, its label and user who assigned it
    """
    
    image = models.ForeignKey(Image)
    user = models.ForeignKey(User)
    # Labels are added later
    label = models.ForeignKey(Label, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
