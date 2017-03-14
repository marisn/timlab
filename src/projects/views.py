# -*- coding: utf-8 -*-
from random import sample

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404
from django.shortcuts import render

from projects.models import Project, UsersProject
from images.models import ImageLabel, Image


class ProjectsListView(ListView):
    model = Project
    order = ('is_active', 'created')


class ProjectDetailView(DetailView):
    model = Project
    
    def get_unlabeled(self):
        """
        Returns URL of one of unlabeled images for particular user
        """
        
        if not self.request.user:
            return None
        
        im_pk = ImageLabel.objects.filter(user=self.request.user, label__isnull=True).values_list('id', flat=True).first()
        if im_pk:
            return '/p/%s/image/%s/' % (self.object.slug, im_pk)
        else:
            return None
    
    def get_usersproject(self):
        """
        Return userproject object for current user
        """
        if not self.request.user:
            return None
        
        up = UsersProject.objects.filter(user=self.request.user, project=self.object).first()
        return up


class JoinProjectView(LoginRequiredMixin, TemplateView):
    template_name = 'projects/project_join.html'
    
    def post(self, request, *args, **kwargs):
        try:
            project = Project.objects.get(slug=kwargs['slug'])
        except Project.DoesNotExist:
            raise Http404("Project does not exist!")
        
        up = UsersProject.objects.filter(user=self.request.user, project=project).first()
        if up:
            return render(request, self.template_name, {
                'message': "You already have joined this project.",
                'project': project
            })
        
        up = UsersProject(user=self.request.user, project=project)
        up.save()
        
        im_set = Image.objects.filter(project=project)
        # Choose random images from all available
        im_ids = sample(xrange(len(im_set)), project.train_count)
        for i in im_ids:
            il = ImageLabel(image=im_set[i], user=self.request.user, project=project)
            il.save()
        
        return render(request, self.template_name, {
            'message': "You have joined the %s project!" % (project.title),
            'project': project,
            'first_img': '/p/%s/image/%s/' % (project.slug, il.pk)
        })
