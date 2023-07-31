from django.urls import path
from download.api_views import MapDownloadView

urlpatterns = [
    path('can-download-map/', MapDownloadView.as_view()),
]
