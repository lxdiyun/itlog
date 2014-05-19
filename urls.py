from django.conf.urls import patterns, url, include

from rest_framework import routers

from views import ResourceViewSet, ResourceStatisticViewSet

router = routers.DefaultRouter()
router.register(r'resource_statistic',
                ResourceStatisticViewSet,
                base_name='resource_statistic')
router.register(r'resource', ResourceViewSet, base_name="resource")

urlpatterns = patterns('',

                       # restful api
                       #url(r'^api/resource_statistic', ResourceStatisticView.as_view()),
                       url(r'^api/', include(router.urls)),
                       url(r'^api-auth/', include('rest_framework.urls',
                                                  namespace='rest_framework'))
                       )
