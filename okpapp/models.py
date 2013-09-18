from django.contrib import admin
from django.db import models


class Application(models.Model):
    email_address = models.EmailField()
    facebook_url = models.CharField(max_length=300)
    requests = models.TextField()
    apply_datetime = models.DateTimeField(auto_now_add=True)
    stripe_token = models.TextField(max_length=400)
    charged = models.BooleanField(default=False)
    description = models.TextField(null=True)

    def __unicode__(self):
        display_text = self.email_address
        if self.description is not None:
            display_text = "{0} {1}".format(display_text, self.description[:100])
        return display_text

class Location(models.Model):
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=400, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Date(models.Model):
    first_application = models.ForeignKey(Application, related_name='first_application')
    second_application = models.ForeignKey(Application, related_name='second_application')
    location = models.ForeignKey(Location, null=True)
    date = models.DateTimeField(null=True)
    description = models.TextField(null=True)

    def __unicode__(self):
        if self.description is not None:
            return self.description[:100]
        else:
            return self.first_application.email_address + ' ' + self.second_application.email_address
admin.site.register(Application)
admin.site.register(Date)
admin.site.register(Location)