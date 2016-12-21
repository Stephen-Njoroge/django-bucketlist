'''
 - Using routers to auto generate end points >
 - Using rest_framework_nested_routes to access nested resources >
 - Using rest_framework_jwt to acquire tokens for authentication.
'''

from django.conf.urls import url, include
from bucketlist_api.views import (
    BucketListViewSet, ItemViewSet, UserViewSet, api_root)
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import SimpleRouter
from rest_framework_nested import routers as ns_router

from rest_framework_jwt.views import obtain_jwt_token


user_register = UserViewSet.as_view({
    'post': 'create'
})


router = SimpleRouter()
router.register(r'bucketlists', BucketListViewSet)

item_router = ns_router.NestedSimpleRouter(
    router, r'bucketlists', lookup='bucketlist')
item_router.register(r'items', ItemViewSet)


urlpatterns = format_suffix_patterns([
    url(r'^$', api_root),
    url(r'^auth/register', user_register),
    url(r'^auth/login', obtain_jwt_token),
    url(r'^', include(router.urls)),
    url(r'^', include(item_router.urls)),

])

# To enable the login button on the django auto doc to work by using
# default drf urls
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework'))]
