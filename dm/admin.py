# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from dm.models import *

admin.site.register(MyModel, admin.ModelAdmin)
admin.site.register(ModelY, admin.ModelAdmin)
