from django.contrib import admin
from django.db import models


class Application(models.Model):
    email_address = models.EmailField()
    facebook_url = models.CharField(max_length=300)
    requests = models.TextField()
    apply_datetime = models.DateTimeField(auto_now_add=True)
    stripe_token = models.TextField(max_length=400)
    charged = models.BooleanField(default=False)

    def __unicode__(self):
        return self.email_address
class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=400, null=True, blank=True)


class Date(models.Model):
    first_application = models.ForeignKey(Application, related_name='first_application')
    second_application = models.ForeignKey(Application, related_name='second_application')
    location = models.ForeignKey(Location, null=True)
    date = models.DateTimeField(null=True)
    def __unicode__(self):
        return '{0} + {0}'.format(self.first_application.email_address,
                                  self.second_application.email_address)

admin.site.register(Application)
admin.site.register(Date)
admin.site.register(Location)