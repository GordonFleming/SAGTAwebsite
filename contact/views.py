from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import base
import os

def index(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']
        full_message = 'From: {name} <{email}>\n\n{message}'.format(name=name, email=email, message=message)
        
        send_mail(
            'Contact Form',
            full_message,
            'website@sagta.org.za',
            #['help@sagta.org.za'],
            [os.environ.get('TO_EMAIL')],
            fail_silently=False,
            )
    return render(request, 'contact/contact_page.html')