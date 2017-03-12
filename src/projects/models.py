# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


@python_2_unicode_compatible
class Project(models.Model):
    """
    Image labeling project
    """
    
    slug = models.SlugField(unique=True, blank=True,
        help_text="Will be provided automaticly if left blank.")
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True,
        help_text="Can contain HTML. Will be placed inside a DIV element.")
    is_active = models.BooleanField(default=True,
        help_text="Unset to disable further labeling.")
    train_count = models.IntegerField(verbose_name="Training image count",
        help_text="Number of images to show for a single user.")
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        
        super(Project, self).save(*args, **kwargs)
    
    def __str__(self):
        return self.title
    

@python_2_unicode_compatible
class Label(models.Model):
    """
    Labels available in a project
    """
    
    text = models.CharField(max_length=50,
        help_text="Short text shown as a choice.")
    code = models.CharField(max_length=20, blank=True,
        help_text="Unique code representing this label.")
    description = models.TextField(blank=True,
        help_text="Longer description to explain meaning of label." +
        "Can contain HTML. Will be placed inside a DIV element.")
    project = models.ForeignKey(Project,
        help_text="A project offering this label as a choice to user.")
    
    class Meta:
        unique_together = ('code', 'project')
        
    def save(self, *args, **kwargs):
        if not self.code:
            self.code = slugify(self.text)
        
        super(Label, self).save(*args, **kwargs)
    
    def __str__(self):
        if self.code:
            return "%s (%s - %s)" % (self.text, self.code, self.project.title)
        return "%s (%s)" % (self.text, self.project.title)


class UsersProject(models.Model):
    """
    Links Users with Projects
    """
    
    completed_imgs = models.IntegerField(default=0,
        help_text="How many images have been labeled.")
    user = models.ForeignKey(User)
    project = models.ForeignKey(Project)
    joined = models.DateTimeField(auto_now_add=True)
