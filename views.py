from django.db.models import Count

from rest_framework import viewsets, filters
from rest_framework.response import Response

from models import Resource
from serializers import ResourceStatisticSerializer


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    model = Resource
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ['name', 'sn', 'sn2', 'catalog_id', 'national_id',
                     'number', 'record_date']
    ordering_fields = '__all__'
    ordering = ['-record_date']
    search_fields = ['name', 'model', 'specification', 'catalog_id',
                     'national_id', 'user', 'sn', 'sn2']


class ResourceStatisticViewSet(ResourceViewSet):
    serializer_class = ResourceStatisticSerializer
    paginate_by = None

    def statistic(self, object_list):
        qs = object_list
        qs = qs.values('record_date', 'name')
        qs = qs.extra(select={'year': "strftime('%Y', record_date)"})
        qs = qs.values('year', 'name').order_by('year', 'name')
        qs = qs.annotate(count=Count('record_date'))

        return qs

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        self.object_list = self.statistic(self.object_list)
        serializer = self.get_serializer(data=self.object_list, many=True)

        columns = set()
        rows = dict()
        if serializer.is_valid():
            row = {'year': "", 'count': 0}
            for d in serializer.data:
                columns.add(d['name'])
                year = d['year']
                row = None
                if year in rows:
                    row = rows[year]
                else:
                    row = dict()
                    row['year'] = year
                    row['count'] = 0

                row[d['name']] = d['count']
                row['count'] += d['count']

                rows[year] = row

                print(row['count'], d['count'], d['name'], d['year'])

        return Response({'columns': columns, 'rows': rows.values()})
