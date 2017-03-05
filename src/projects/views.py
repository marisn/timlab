# -*- coding: utf-8 -*-
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView

from projects.models import Project
from images.models import ImageLabel


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
        
        im_pk = ImageLabel.objects.filter(user=self.request.user, label__is_null=False).first()
        return '/p/%s/image/%s/' % (self.object.slug, im_pk)
