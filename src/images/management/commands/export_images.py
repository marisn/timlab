# -*- coding: utf-8 -*-
import os
from shutil import copy
from random import shuffle

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from projects.models import Project
from images.models import ImageLabel


class Command(BaseCommand):
    """
    Usage example:
    ./manage.py export_images 2 24 /home/user/labeled_images/
    """
    
    help = "Writes out labeled images for Keras"
    
    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int)
        parser.add_argument('user_id', type=int)
        parser.add_argument('target', type=str)
    
    def handle(self, *args, **options):
        try:
            project = Project.objects.get(pk=options['project_id'])
        except Project.DoesNotExist:
            raise CommandError('Project "%s" does not exist' % options['project_id'])
        
        try:
            user = User.objects.get(pk=options['user_id'])
        except User.DoesNotExist:
            raise CommandError('User "%s" does not exist' % options['user_id'])
        
        if not os.path.isdir(options['target']):
            try:
                os.makedirs(options['target'])
            except os.error:
                raise CommandError("Failed to create output directory <%s>." % options['target'])
        
        for label in project.label_set.all():
            try:
                os.makedirs(os.path.join(options['target'], 'test', label.code))
                os.makedirs(os.path.join(options['target'], 'valid', label.code))
                os.makedirs(os.path.join(options['target'], 'train', label.code))
            except os.error:
                raise CommandError("Failed to create output directory <%s>." %
                os.path.join(options['target'], 'test', label.code))
        
        imgs = ImageLabel.objects.filter(project=project, user=user).select_related('label', 'image')
        rnd = range(len(imgs))
        shuffle(rnd)
        test_count = int((20 * len(imgs)) / 100)
        train_up = len(imgs) - 2 * test_count
        valid_up = train_up + test_count
        
        # Include validation into training
        for i in rnd[0:valid_up]:
            img = imgs[i]
            dst = os.path.join(options['target'], 'train', img.label.code)
            try:
                copy(img.image.filename, dst)
            except os.error:
                raise CommandError("Copy failed from <%s> to <%s>." % (img.image.filename, dst))
        
        for i in rnd[train_up:valid_up]:
            img = imgs[i]
            dst = os.path.join(options['target'], 'valid', img.label.code)
            try:
                copy(img.image.filename, dst)
            except os.error:
                raise CommandError("Copy failed from <%s> to <%s>." % (img.image.filename, dst))
        
        for i in rnd[valid_up:]:
            img = imgs[i]
            dst = os.path.join(options['target'], 'test', img.label.code)
            try:
                copy(img.image.filename, dst)
            except os.error:
                raise CommandError("Copy failed from <%s> to <%s>." % (img.image.filename, dst))
