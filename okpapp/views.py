import json
from django.http import HttpResponse
from django.shortcuts import render_to_response, render, redirect
from models import Application


def home(req):
    return render_to_response('index.html')


def application(req):
    if req.method != 'POST':
        return redirect('/')
    application = Application()
    application.email_address = req.POST.get('emailAddress')
    application.facebook_url = req.POST.get('facebookUrl')
    application.requests = req.POST.get('specialRequests')
    application.stripe_token = req.POST.get('stripeToken')
    application.save()
    return HttpResponse('{"message": "thanks"}', status=200)