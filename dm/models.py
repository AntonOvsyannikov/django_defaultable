# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from dm.defaultable.models import Defaultable


# class ModelX(Defaultable):
#     def __unicode__(self):
#         return "{}X{}".format(self.mark, self.id)

class ModelY(Defaultable):
    def __unicode__(self):
        return "{}Y{}".format(self.mark, self.id)

# -------------------------------------------

class MyModel(models.Model):
    # x = ModelX.ForeignKey()
    y = ModelY.ForeignKey()

    def __unicode__(self):
        return "M{}:y={}".format(self.id, self.y)



