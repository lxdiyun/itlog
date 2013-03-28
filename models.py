from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User as Operator


class User(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('item user'))

    class Meta:
        verbose_name = _('item user')
        verbose_name_plural = _('item users')

    def __unicode__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(max_length=250, verbose_name=_('location'))

    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')

    def __unicode__(self):
        return self.name


class Log(models.Model):
    date = models.DateField(auto_now_add=True,
                            verbose_name=_('date'))
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name=_("description"))
    operator = models.ForeignKey(Operator, verbose_name=_('operator'))
    item = models.ForeignKey('Item')

    class Meta:
        verbose_name = _('log')
        verbose_name_plural = _('logs')

    def __unicode__(self):
        return self.description


class Item(models.Model):
    STATUS = (
        (0, _('store up')),
        (1, _('in use')),
        (2, _('scrap')),
    )
    name = models.CharField(max_length=250, verbose_name=_('item name'))
    sn = models.CharField(max_length=128,
                          null=True,
                          blank=True,
                          verbose_name=_('sn'))
    sn2 = models.CharField(max_length=128,
                           null=True,
                           blank=True,
                           verbose_name=_('sn/2'))
    status = models.IntegerField(max_length=8,
                                 choices=STATUS,
                                 default=0,
                                 verbose_name=_('status'))
    comments = models.TextField(blank=True,
                                null=True,
                                verbose_name=_('comments'))
    buy_date = models.DateField(null=True,
                                blank=True,
                                verbose_name=_('buy date'))
    last_modify_date = models.DateField(auto_now_add=True,
                                        verbose_name=_('last modify date'))
    last_modify_by = models.ForeignKey(Operator,
                                       verbose_name=_('last modify by'))
    user = models.ForeignKey(User)
    location = models.ForeignKey(Location)

    class Meta:
        ordering = ['-last_modify_date']
        verbose_name = _('item')
        verbose_name_plural = _('items')

    def __unicode__(self):
        return self.name
