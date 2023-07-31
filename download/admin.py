from django.contrib import admin
from download.models import MapDownload


class MapDownloadAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'download_date'
    )
    list_filter = (
        'user',
    )


# Register your models here.
admin.site.register(MapDownload, MapDownloadAdmin)
