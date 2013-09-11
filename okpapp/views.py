import json
import smtplib
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, redirect
from models import Application
from okpedro.settings import GMAIL_PASSWORD, GMAIL_USER


def home(req):
    context_instance = {}
    context_instance.update(csrf(req))
    return render_to_response('index.html', context_instance)


def application(req):
    if req.method != 'POST':
        return redirect('/')
    application = Application()
    application.email_address = req.POST.get('emailAddress')
    application.facebook_url = req.POST.get('facebookUrl')
    application.requests = req.POST.get('specialRequests')
    application.stripe_token = req.POST.get('stripeToken')
    application.save()
    send_email(application)
    return HttpResponse('{"message": "thanks"}', status=200)


def send_email(application):
    body_html = '<html> ' \
                       '<meta http-equiv="Content-Type" content="text/html charset=UTF-8" />' \
                       '<head><style>body {font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;}</style></head>' \
                       '<body><h3>Thanks for applying!</h3>'
    body_html += '<div><img src="https://okpedro.trillworks.com/static/img/pedrosmall.jpg"></div>'
    body_html += '<p>I\'ll add you on Facebook so I can find a good date for you. ' \
                 'Make sure you add me back.</p>'
    body_html+= '<p>Pedro</p>'
    body_html += '</body></html>'
    subject = 'Pedro has received your application!'
    message = """Content-Type: text/html\nFrom: %s\nTo: %s\nSubject: %s\n\n%s

            """ % ('Pedro', ", ".join([application.email_address]),
                   subject, body_html)
    session = smtplib.SMTP('smtp.gmail.com:587')
    session.ehlo()
    session.starttls()
    session.login(GMAIL_USER, GMAIL_PASSWORD)
    session.sendmail('pedro@trillworks.com', [application.email_address], message)
    session.quit()
