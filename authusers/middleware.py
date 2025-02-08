from django.shortcuts import render
from django.http import HttpResponse
from mysite.settings.base import WAGTAIL_FRONTEND_LOGIN_URL

class PermissionDeniedMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Check if it's a redirect to login page with a 'next' parameter
        if (response.status_code == 302
            and 
            response.url.startswith(WAGTAIL_FRONTEND_LOGIN_URL) and 
            request.user.is_authenticated):
            
            # Return a script that shows alert and redirects
            return HttpResponse(
                '<script>'
                'alert("You don\'t have permission to access this page.");'
                'window.location.href="/";'  # Redirect to home page
                '</script>'
            )
            
        return response