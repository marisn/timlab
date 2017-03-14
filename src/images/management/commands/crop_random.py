# -*- coding: utf-8 -*-
import os
import random
import fnmatch

from PIL import Image

from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """
    Usage example:
    ./manage.py crop_random 4 256 0.5 /home/user/images ./media/project1/
    """
    help = "Crops N random images from each of image files"
    
    def add_arguments(self, parser):
        parser.add_argument('count', type=int,
            help="Number of samples to cut out from a single file")
        parser.add_argument('size', type=int, default=256,
            help="Size of sampled image (defaults to 256)")
        parser.add_argument('ratio', type=float, default=1.0,
            help="Shrink image by ratio before cropping a sample (defaults to 1 = no shrink")
        parser.add_argument('source', type=str,
            help="Path to folder containing images to crop")
        parser.add_argument('target', type=str,
            help="Path where to store result (i.e. ./MEDIA_ROOT/project_slug/)")
    
    def handle(self, *args, **options):
        if not options['count'] > 0:
            raise CommandError("Count must be larger than 0")
        
        if not options['size'] > 3:
            raise CommandError("Size of sample images should be larger than 3x3 pixels")
        
        if not (options['ratio'] >= 0 and options['ratio'] <= 1):
            raise CommandError("Resize ratio value should be in range from 0 (=size parameter) to 1 (=original size)")
        
        if options['ratio'] == 0 and options['count'] > 1:
            raise CommandError("Resizing original to sample size and requesting multiple samples doesn't make sense")
        
        if not os.path.isdir(options['target']):
            try:
                os.makedirs(options['target'])
            except os.error:
                raise CommandError("Failed to create output directory <%s>." % options['target'])
        
        for path, dirs, files in os.walk(options['source']):
            match = []
            match.extend(fnmatch.filter(files, '*.[Jj][Pp][Gg]'))
            match.extend(fnmatch.filter(files, '*.[Jj][Pp][Ee][Gg]'))
            match.extend(fnmatch.filter(files, '*.[Pp][Nn][Gg]'))
            match.extend(fnmatch.filter(files, '*.[Tt][Ii][Ff]'))
            match.extend(fnmatch.filter(files, '*.[Tt][Ii][Ff][Ff]'))
            
            for m in match:
                im = Image.open(os.path.join(path, m))
                
                # Resize image along the shortest edge
                if options['ratio'] < 1:
                    w, h = im.size
                    a = int(w * options['ratio'] + options['size'])
                    b = int(h * options['ratio'] + options['size'])
                    rim = im.resize((a, b), Image.ANTIALIAS)
                else:
                    rim = im
                
                for i in range(options['count']):
                    out = rim.crop(self.get_random_box(rim.size, options['size']))
                    outname = '%s_%s.png' % (os.path.splitext(m)[0], i)
                    try:
                        out.save(os.path.join(options['target'], outname))
                    except:
                        raise CommandError("There was an error writing <%s>." %
                            os.path.join(options['target'], outname))
        
    def get_random_box(self, im_size, size):
        width, height = im_size
        a = width - size
        b = height - size
        l = random.randint(0, a)
        t = random.randint(0, b)
        
        return (l, t, l + size, t + size)
