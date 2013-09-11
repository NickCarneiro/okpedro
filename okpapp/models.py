from django.db import models


class Application(models.Model):
    email_address = models.EmailField()
    facebook_url = models.CharField(max_length=300)
    requests = models.TextField()
    apply_datetime = models.DateTimeField(auto_now_add=True)
    stripe_token = models.TextField(max_length=400)
