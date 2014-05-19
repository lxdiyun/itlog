from django.db.models import Count, Sum

from rest_framework import viewsets, filters
from rest_framework.response import Response

from models import Resource
from serializers import ResourceSerializer, ResourceStatisticSerializer


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    model = Resource
    serializer_class = ResourceSerializer
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ['name', 'catalog_id', 'national_id', 'record_date']
    ordering_fields = '__all__'
    ordering = ['-record_date']
    search_fields = ['name', 'model', 'specification', 'catalog_id',
                     'national_id', 'user', 'sn', 'sn2', 'record_date']


class ResourceStatisticViewSet(ResourceViewSet):
    serializer_class = ResourceStatisticSerializer
    paginate_by = None

    def statistic(self, object_list):
        qs = object_list
        qs = qs.values('record_date', 'name', 'price')
        qs = qs.extra(select={'year': "strftime('%%Y', record_date)"})
        qs = qs.values('year', 'name').order_by('name')
        qs = qs.annotate(count=Count('record_date'), total_price=Sum('price'))

        return qs

    def list(self, request, *args, **kwargs):
        self.object_list = self.filter_queryset(self.get_queryset())
        self.object_list = self.statistic(self.object_list)
        serializer = self.get_serializer(data=self.object_list, many=True)
        result = None

        if serializer.is_valid():
            def reduce_rows(result, d):
                year = d['year']
                row = None
                if year in result:
                    row = result[year]
                else:
                    row = dict({'total': {'count': 0, 'total_price': 0}})

                row[d['name']] = {"count": d['count'],
                                  "total_price": d['total_price']}
                row['total']['count'] += d['count']
                row['total']['total_price'] += d['total_price']

                result[year] = row

                return result

            result = (reduce(reduce_rows, serializer.data, dict()))

        return Response(result)
