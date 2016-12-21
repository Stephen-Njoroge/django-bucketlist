from rest_framework import permissions

from bucketlist_api.models import BucketList


class IsParentId(permissions.BasePermission):
    """
    To deny clients access to other users bucketlists
    """

    def has_permission(self, request, view):
        try:
            owner = BucketList.objects.get(
                pk=view.kwargs['bucketlist_pk']).owner
            return request.user == owner
        except BucketList.DoesNotExist:
            return True


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, BucketList):
            return obj.owner == request.user
