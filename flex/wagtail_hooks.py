# Don't download files hook

from django.http import HttpResponse
from wagtail.core import hooks
from django.shortcuts import redirect

@hooks.register('before_serve_document')
def serve_pdf(document, request):
    """Forces open in browser view before download"""

    if document.file_extension != 'pdf':
        return  # Empty return results in the existing response
    response = HttpResponse(document.file.read(), content_type='application/pdf')
    response['Content-Disposition'] = 'filename="' + document.file.name.split('/')[-1] + '"'
    if request.GET.get('download', False) in [True, 'True', 'true']:
        response['Content-Disposition'] = 'attachment; ' + response['Content-Disposition']
    return response