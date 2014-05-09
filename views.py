from django.db.models import Count

from rest_framework import viewsets, generics, filters

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


class ResourceStatisticView(generics.ListAPIView):
    serializer_class = ResourceStatisticSerializer
    queryset = Resource.objects

    def get_queryset(self):
        qs = self.queryset
        qs = qs.values('record_date')
        qs = qs.extra(select={'year': "strftime('%Y', record_date)"})
        qs = qs.values('year').order_by('year')
        qs = qs.annotate(count=Count('record_date'))
