from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import permissions

from download.models import MapDownload


class CanDownloadMaps(permissions.BasePermission):

    def has_permission(self, request, view):
        # Check if the current user is part of the 'Members' group
        return request.user.groups.filter(name='Members').exists()


class MapDownloadView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        TokenHasReadWriteScope]

    def get(self, request, format=None):
        if request.user.groups.filter(name='Members').exists():
            allowed = True
        else:
            map_downloads = MapDownload.objects.filter(
                user=request.user,
                download_date__year=datetime.now().year
            )
            if not map_downloads.exists() or map_downloads.count() < 2:
                allowed = True
                MapDownload.objects.create(
                    user=request.user
                )
            else:
                allowed = False

        return Response({
            'allowed': allowed
        })
