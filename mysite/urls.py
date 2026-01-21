from django.conf import settings
from django.contrib import admin
from django.urls import include, path


from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from auth.views import CustomLogoutView

from .api import api_router, UserInfo



urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('user_info/', UserInfo.as_view()),
    path('o/', include('oauth2_provider.urls', namespace='oauth2_provider')),

    path('', include('allauth.urls')),
    path('accounts/logout/', CustomLogoutView.as_view(), name='account_logout'),
    path('accounts/', include('allauth.urls')),
    path('', include('django.contrib.auth.urls')),
    path('', include('download.urls')),

    path('api/custom/', include('authusers.urls')),
    path('payments/', include('payments.urls')),
    path('api/v2/', api_router.urls),

    path("", include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path(r"^pages/", include(wagtail_urls)),
]
