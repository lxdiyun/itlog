from models import *
from django.contrib import admin
from daterange_filter.filter import DateRangeFilter
from datetime import datetime


class ItemTypeAdmin(admin.ModelAdmin):
    model = ItemType
    list_display = ['id', 'name']


class ManufacturerAdmin(admin.ModelAdmin):
    model = Manufacturer
    list_display = ['id', 'name']


class UserAdmin(admin.ModelAdmin):
    model = User
    list_display = ['id', 'name']


class LocationAdmin(admin.ModelAdmin):
    model = Location
    list_display = ['id', 'name']


class LogInline(admin.TabularInline):
    model = Log
    readonly_fields = ['operator', 'date']

    def save_model(self, request, obj, form, change):
        print("new log")
        obj.operator = request.user
        super(LogInline, self).save(request, obj, form, change)


class ItemAdmin(admin.ModelAdmin):
    list_display = ['name',
                    'sn',
                    'sn2',
                    'buy_date',
                    'last_modify_date',
                    'last_modify_by',
                    'user',
                    'location',
                    'comments']
    search_fields = ['name', 'comments', 'user', 'location', 'sn', 'sn2']
    list_filter = [('last_modify_date', DateRangeFilter),
                   'last_modify_by',
                   'user__name',
                   'location__name',
                   ('buy_date', DateRangeFilter),
                   ]
    inlines = [LogInline]
    exclude = ['last_modify_by']

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
            message += "\n%s => %s" % (item, form.cleaned_data.get(item))

        return message


admin.site.register(Item, ItemAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(User, UserAdmin)
admin.site.register(Location, LocationAdmin)
