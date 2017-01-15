import os
import sys
sys.path = ['/var/www/GadgetFreak'] + sys.path
os.environ['DJANGO_SETTINS_MODULE'] = 'GadgetFreak.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
