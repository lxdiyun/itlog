# Create your views here.

from rest_framework import viewsets

from models import Resource


class ResourceViewSet(viewsets.ReadOnlyModelViewSet):
    model = Resource
