from django.db import models
from django.contrib import admin

from .models import *

admin.site.site_header = 'The Backbone Group'

admin.site.register(HelpRequest)
