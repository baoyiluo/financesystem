# -*- coding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
# Create your models here.
class Finance(models.Model):
    ACCOUNT_CHOICE = (
        ('-1', _(u"出账")),
        ('1', _(u"入账"))
    )
    startperson = models.ForeignKey(User)
    maneycount = models.DecimalField(max_digits=8,decimal_places=2)
    financename = models.CharField(_('name'), max_length=80)
    financeintro = models.CharField(_('intro'), max_length=80)
    examineperson = models.ManyToManyField(User, null=True, blank=True, related_name="examineperson", verbose_name=_("users"))
    financetype = models.CharField(_('financetype'), max_length=80, choices=ACCOUNT_CHOICE)
    status = models.BooleanField(_("Status"), default=True)
