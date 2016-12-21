from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view
from rest_framework import permissions

from bucketlist_api.serializers import (
    BucketListSerializer, ItemSerializer, UserSerializer)
from bucketlist_api.models import BucketList, Item
from bucketlist_api.permissions import IsOwner, IsParentId

from django.contrib.auth.models import User

# Create your views here.


@api_view(['GET'])
def api_root(request, format=None):
    '''Ease the case of any need to change the urls'''
    return Response({
        'bucketlists': reverse('bucketlists', request=request, format=format),
        'items': reverse('items', request=request, format=format)
    })


class BucketListViewSet(viewsets.ModelViewSet):
    '''
    API view to perform CRUD operations on Bucketlists.
    POST = CREATE,
    GET = READ,
    PUT = UPDATE,
    DELETE = DELETE.
    Requires authorization and bucketlist pk to read/update/delete
    a specific bucketlist.
    Users can only access their personal Bucketlists.
    '''

    queryset = BucketList.objects.all()
    serializer_class = BucketListSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsOwner)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def list(self, request):
        queryset = request.user.bucketlists.all()
        serializer = BucketListSerializer(
            queryset, many=True, context={'request': Request(request)})
        return Response(serializer.data)


class ItemViewSet(viewsets.ModelViewSet):
    '''
    API view to perform CRUD operations on Bucketlist Items.
    POST = CREATE,
    GET = READ,
    PUT = UPDATE,
    DELETE = DELETE.
    Requires authorization, bucketlist pk of bucketlist holding the item,
    and item pk of the item to read/update/delete.
    Items are tied to mother bucketlists.
    '''

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    permission_classes = (permissions.IsAuthenticated, IsParentId)

    def perform_create(self, serializer):
        item_bucketlist_id = self.kwargs.get("bucketlist_pk")
        bucketlist = BucketList.objects.get(id=item_bucketlist_id)
        serializer.save(bucketlist=bucketlist)

    def get_queryset(self):

        bucketlist_id = self.kwargs.get('bucketlist_pk')
        return Item.objects.filter(
            bucketlist=bucketlist_id,
            bucketlist__owner=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    '''
    Users view to allow registration of a user by sending a
    unique username, a password, and an email.
    '''

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.AllowAny,)
