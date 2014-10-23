from import_export import resources, fields, widgets
from .models import Resource
from datetime import datetime, timedelta


def excel_date_to_datetime(excel_date):
    return datetime(1899, 12, 30) + timedelta(days=int(excel_date))


class DateField(fields.Field):
    def clean(self, data):
        value = super(DateField, self).clean(data)
        value = excel_date_to_datetime(value)
        return value


class NotNullWidget(widgets.Widget):
    def clean(self, value):
        cleaned_value = super(NotNullWidget, self).clean(value)
        if not cleaned_value:
            cleaned_value = 0

        return cleaned_value


class ResourceResource(resources.ModelResource):
    buy_date = DateField(attribute="buy_date", column_name="buy_date")
    record_date = DateField(attribute="record_date", column_name="record_date")
    depreciated_price = fields.Field(attribute="depreciated_price",
                                     column_name="depreciated_price",
                                     widget=NotNullWidget())
    used_year = fields.Field(attribute="used_year",
                             column_name="used_year",
                             widget=NotNullWidget())

    class Meta:
        model = Resource
