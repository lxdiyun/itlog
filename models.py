from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User as Operator
from django.utils.timezone import localtime


class Manufacturer(models.Model):
    name = models.CharField(max_length=250,
                            verbose_name=_('manufacturer name'))

    class Meta:
        verbose_name = _('manufacturer')
        verbose_name_plural = _('manufacturers')

    def __unicode__(self):
        return self.name


class ItemType(models.Model):
    name = models.CharField(max_length=250,
                            verbose_name=_('item type name'))

    class Meta:
        verbose_name = _('item type')
        verbose_name_plural = _('item types')

    def __unicode__(self):
        return self.name


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
    time = models.DateTimeField(auto_now_add=True,
                                verbose_name=_('log time'))
    description = models.TextField(blank=True,
                                   null=True,
                                   verbose_name=_("description"))
    operator = models.ForeignKey(Operator, verbose_name=_('operator'))
    item = models.ForeignKey('Item')

    class Meta:
        ordering = ['-time']
        verbose_name = _('log')
        verbose_name_plural = _('logs')

    def __unicode__(self):
        return "%s|%s|%s" % (localtime(self.time),
                             self.operator,
                             self.description)


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
    user = models.ForeignKey(User, verbose_name=_('item user'))
    location = models.ForeignKey(Location, verbose_name=_('location'))
    itemtype = models.ForeignKey(ItemType, verbose_name=_('item type'))
    manufacturer = models.ForeignKey(Manufacturer,
                                     verbose_name=_('manufacturer'))

    class Meta:
        ordering = ['-last_modify_date']
        verbose_name = _('item')
        verbose_name_plural = _('items')

    def __unicode__(self):
        return self.name

    def get_recent_logs(self):
        string = ""
        for log in self.log_set.all()[:5]:
            string += "#" + unicode(log) + "\n <br> \n"

        return string
    get_recent_logs.short_description = _('recent logs')
    get_recent_logs.allow_tags = True
