from models import *
from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from datetime import datetime
from adli.admin_actions import export_csv_action, clone_action


class ItemTypeAdmin(admin.ModelAdmin):
    model = ItemType
    list_display = ['name']


class ManufacturerAdmin(admin.ModelAdmin):
    model = Manufacturer
    list_display = ['name']


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['name']


class LocationAdmin(admin.ModelAdmin):
    model = Location
    list_display = ['name']


class LogInline(admin.TabularInline):
    model = Log
    readonly_fields = ['operator', 'time']

    def save_model(self, request, obj, form, change):
        obj.operator = request.user
        super(LogInline, self).save(request, obj, form, change)


class ItemAdmin(admin.ModelAdmin):
    list_display = ([f.name for f in Item._meta.fields]
                    + ['get_recent_logs'])
    search_fields = ['name', 'comments', 'user__name', 'location__name',
                     'item_type__name', 'manufacturer__name', 'sn', 'sn2',
                     'log__description']
    list_filter = [('last_modify_date', DateRangeFilter),
                   ('buy_date', DateRangeFilter),
                   'last_modify_by',
                   'status',
                   'user__name',
                   'location__name',
                   'manufacturer__name',
                   'item_type__name',
                   ]
    inlines = [LogInline]
    exclude = ['last_modify_by']
    actions = [export_csv_action(extra=['get_recent_logs'],
                                 exclude=['id']),
               clone_action()]

    def save_model(self, request, obj, form, change):
        obj.last_modify_by = request.user
        obj.last_modify_date = datetime.now()
        obj.save()

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)

        for instance in instances:
            # Check if it is the correct type of inline
            if isinstance(instance, Log):
                if not instance.operator_id:
                    instance.operator = request.user

                instance.save()

    def construct_change_message(self, request, form, formsets):
        message = super(ItemAdmin, self).construct_change_message(request,
                                                                  form,
                                                                  formsets)
        print(form.cleaned_data)
        for item in form.changed_data:
            message += "\n%s => %s" % (item,
                                       unicode(form.cleaned_data.get(item)))

        return message

    def clone(self, obj, request):
            new_kwargs = dict()
            exclude = ['id', 'last_modify_by', 'last_modify_date']
            for fld in self.model._meta.fields:
                if fld.name not in exclude:
                    new_kwargs[fld.name] = getattr(obj, fld.name)

            new_kwargs['last_modify_by'] = request.user
            new_kwargs['last_modify_date'] = datetime.now()

            self.model.objects.create(**new_kwargs)


class ResourceAdmin(admin.ModelAdmin):
    search_fields = ['name', 'user', 'sn', 'sn2']
    list_filter = [('record_date', DateRangeFilter),
                   ('buy_date', DateRangeFilter),
                   'catalog_id',
                   'national_id',
                   'user',
                   'name',
                   'funding_source',
                   ]

    def get_list_display(self, request):
        l = [f.name for f in Resource._meta.fields]
        l.remove('id')
        l = l + ['get_item']

        return l

admin.site.register(Item, ItemAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Resource, ResourceAdmin)
