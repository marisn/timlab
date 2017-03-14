# -*- coding: utf-8 -*-
import os
import fnmatch

from django.core.management.base import BaseCommand, CommandError

from projects.models import Project
from images.models import Image


class Command(BaseCommand):
    """
    Usage example:
    ./manage.py import_images 2 media/project2/
    """
    
    help = "Populates projects file list with images from a folder"
    
    def add_arguments(self, parser):
        parser.add_argument('project_id', type=int)
        parser.add_argument('folder', type=str)
    
    def handle(self, *args, **options):
        try:
            project = Project.objects.get(pk=options['project_id'])
        except Project.DoesNotExist:
                raise CommandError('Project "%s" does not exist' % options['project_id'])
        
        for path, dirs, files in os.walk(options['folder']):
            match = []
            match.extend(fnmatch.filter(files, '*.[Jj][Pp][Gg]'))
            match.extend(fnmatch.filter(files, '*.[Jj][Pp][Ee][Gg]'))
            match.extend(fnmatch.filter(files, '*.[Pp][Nn][Gg]'))
            match.extend(fnmatch.filter(files, '*.[Tt][Ii][Ff]'))
            match.extend(fnmatch.filter(files, '*.[Tt][Ii][Ff][Ff]'))
            
            for m in match:
                im = Image(filename=os.path.join(path, m), project=project)
                im.save()
