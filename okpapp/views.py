import smtplib
from django.core import serializers
from django.core.context_processors import csrf
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, redirect
import stripe
from models import Application, Date
from okpedro.settings import GMAIL_PASSWORD, GMAIL_USER, STRIPE_API_KEY

stripe.api_key = STRIPE_API_KEY
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


def manage(req):
    apps = Application.objects.filter()
    dates = Date.objects.filter()
    return render_to_response('manage.html', {'applications': apps, 'dates': dates})


def create_date(req):
    if req.method != 'POST':
        return redirect('/')
    app_id_one = req.POST.get('applicationOne')
    app_id_two = req.POST.get('applicationTwo')
    date = Date()
    first_application = Application.objects.get(pk=app_id_one)
    second_application = Application.objects.get(pk=app_id_two)
    date.first_application = first_application
    date.second_application = second_application
    date.save()
    return HttpResponse(serializers.serialize('json', [date]), status=200)

def charge(req):
    if req.method != 'POST':
        return
    app_id = req.POST.get('applicationId')
    application = Application.objects.get(pk=app_id)
    response_message = ''
    response_status = 200
    try:
        charge = stripe.Charge.create(
            amount=2000, # amount in cents, $20
            currency="usd",
            card=application.stripe_token,
            description=application.email_address
        )
        response_message = 'Card successfully charged'
    except stripe.CardError, e:
        # The card has been declined
        response_message = e
        response_status = 500
    return HttpResponse('{"message": "{}"}'.format(response_message), status=response_status)
