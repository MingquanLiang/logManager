from django.conf.urls import patterns, include, url

from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ArchApps.views.home', name='home'),
    # url(r'^ArchApps/', include('ArchApps.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    #user-defined urls
    url(r'^demo_application/', include('demo_application.urls')),

    #TODO: for public urls
    url(r'^media/(?P<downloadFile>.*)/$', 'publicView.downloadAFile'),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include(admin.site.urls)),
    
    #handle static file
    url(r'^static/(?P<path>.*)$','django.views.static.serve', {'document_root':settings.STATIC_ROOT}), 
    
)
