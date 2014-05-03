# Create your views here.

from rest_framework import viewsets, filters

from models import Resource


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    model = Resource
    filter_backends = (filters.DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter)
    filter_fields = ['name', 'sn', 'sn2', 'number', 'record_date']
    ordering_fields = '__all__'
    ordering = ['-record_date']
    search_fields = ['name', 'model', 'specification', 'user', 'sn', 'sn2']
