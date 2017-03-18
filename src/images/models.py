# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html

from projects.models import Label, Project


@python_2_unicode_compatible
class Image(models.Model):
    """
    Reference to a particular image file
    """
    
    filename = models.CharField(max_length=100)
    project = models.ForeignKey(Project)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return '%s (%s)' % (self.filename, self.project.slug)
    
    def preview(self):
        return format_html('<img src="/{}">', self.filename)


class ImageLabel(models.Model):
    """
    Link between image, its label and user who assigned it
    """
    
    image = models.ForeignKey(Image)
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    # Labels are added later
    label = models.ForeignKey(Label, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    
    def get_absolute_url(self):
        return '/p/%s/image/%s' % (self.project.slug, self.pk)
    
    def __str__(self):
        return "%s - %s" % (self.user.username, self.image.filename)
