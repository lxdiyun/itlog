from django.db.models import Count

from rest_framework import viewsets, generics

from models import Resource
from serializers import ResourceStatisticSerializer


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    model = Resource


class ResourceStatisticView(generics.ListAPIView):
    serializer_class = ResourceStatisticSerializer
    queryset = Resource.objects

    def get_queryset(self):
        qs = self.queryset
        qs = qs.values('record_date')
        qs = qs.extra(select={'year': "strftime('%Y', record_date)"})
        qs = qs.values('year').order_by('year')
        qs = qs.annotate(count=Count('record_date'))
