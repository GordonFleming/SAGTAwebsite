from django.shortcuts import render
from django.core.mail import send_mail
import os
from mailersend import emails
import logging

logger = logging.getLogger(__name__)

mailer = emails.NewEmail('')

def index(request):
    logger.info("sdfsd")
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
        

        mail_body = {}

        mail_from = {
            "name": name,
            "email": email,
        }

        recipients = [
            {
                "name": 'SAGTA',
                "email": '',
            }
        ]

        reply_to = {
            "name": 'SAGTA',
            "email": 'contact@sagta.org.za',
        }

        mailer.set_mail_from(mail_from, mail_body)
        mailer.set_mail_to(recipients, mail_body)
        mailer.set_subject("Website contact form submission", mail_body)
        mailer.set_html_content(full_message, mail_body)
        mailer.set_plaintext_content(full_message, mail_body)
        mailer.set_reply_to(reply_to, mail_body)

        mailer.send(mail_body)
        logger.info("Form Data Received:", mailer.send(mail_body))

    return render(request, 'contact/contact_page.html')