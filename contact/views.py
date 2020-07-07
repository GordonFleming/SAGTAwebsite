from django.shortcuts import render
from django.core.mail import send_mail
from django.conf import base

def index(request):
    if request.method == 'POST':
        message = request.POST['name','email','message']
        
        send_mail(
            'Contact Form',
            message,
            'website@sagta.org.za',
            ['flemingrgordon@gmail.com'],
            fail_silently=False,
            )
    return render(request, 'contact/contact_page.html')