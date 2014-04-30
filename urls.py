from django.conf.urls import patterns, url, include

from rest_framework import routers

from views import ResourceViewSet

router = routers.DefaultRouter()
router.register(r'resource', ResourceViewSet)

urlpatterns = patterns('',

                       # restful api
                       url(r'^api/', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls',
                                                  namespace='rest_framework'))
                       )
