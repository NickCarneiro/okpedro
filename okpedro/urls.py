from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'okpapp.views.home', name='home'),
    url(r'^okpedro/', include('okpapp.urls')),
    url(r'^apply', 'okpapp.views.application', name='apply'),
    url(r'^manage', 'okpapp.views.manage', name='manage'),
    url(r'^createDate', 'okpapp.views.create_date', name='createDate'),
    url(r'^charge', 'okpapp.views.charge', name='charge'),
    (r'^accounts/login/$', 'django.contrib.auth.views.login'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
