# -*- coding: utf-8 -*-
from django.views.generic.edit import UpdateView

from images.models import ImageLabel


class ImageLabelUpdateView(UpdateView):
    """
    Images to label should be assigned when an user joins a project.
    Thus now we just need to update labels for unlabeled images.
    """
    
    model = ImageLabel
    fields = ('label', )
    
    def next_unlabeled():
        """
        Returns PK of next unlabeled image or False if there is none.
        """
        
        return self.queryset.filter(label__is_null=False).first()
    
    def get_object(self, *args, **kwargs):
        """
        User can only update his own labels.
        """
        
        obj = super(ImageLabelUpdateView, self).get_object(*args, **kwargs)
        obj = obj.filter(user=self.request.user)
        return obj
    
    def get_success_url(self, *args, **kwargs):
        """
        If there are any unlabaled images, show the next one.
        """
        
        return self.next_unlabeled().get_absolute_url()
