# coding=utf-8
from __future__ import absolute_import
from functools import partial

from django.db import models, IntegrityError
from django.db.models import Q
from django.db.models.signals import pre_delete

class Defaultable(models.Model):
    class Meta:
        abstract = True

    isDefault = models.BooleanField(default=False)

    @classmethod
    def default(cls):
        from .stuff import get_or_create_default
        return partial(get_or_create_default, cls.__name__, cls._meta.app_label)

    @classmethod
    def ForeignKey(cls, **kwargs):
        return models.ForeignKey(cls, default=cls.default(), on_delete=models.SET_DEFAULT)

    # take care of data integrity
    def __init__(self, *args, **kwargs):
        super(Defaultable, self).__init__(*args, **kwargs)

        # noinspection PyShadowingNames,PyUnusedLocal
        def pre_delete_defaultable(instance, **kwargs):
            if instance.isDefault:
                raise IntegrityError, "Can not delete default object {}".format(instance.__class__.__name__)

        pre_delete.connect(pre_delete_defaultable, self.__class__, weak=False, dispatch_uid=self._meta.db_table)

    def save(self, *args, **kwargs):
        super(Defaultable, self).save(*args, **kwargs)
        if self.isDefault:  # Ensure only one default, so make all others non default
            self.__class__.objects.filter(~Q(id=self.id), isDefault=True).update(isDefault=False)
        else:  # Ensure at least one default exists
            if not self.__class__.objects.filter(isDefault=True).exists():
                self.__class__.objects.filter(id=self.id).update(isDefault=True)

    @property
    def mark(self):
        # noinspection PyTypeChecker
        return ['', '*'][self.isDefault]
