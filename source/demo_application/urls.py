from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'ArchApps.views.home', name='home'),
    # url(r'^ArchApps/', include('ArchApps.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url('^$', 'demo_application.views.searchIndex'),
    # search and show the result
    url('^searchIndex/$', 'demo_application.views.searchIndex'),
    url('^searchResult/$', 'demo_application.views.searchResult'),
    # for upload files
    url('^uploadFilename/$', 'demo_application.views.uploadFilename'),
    url('^echoUploadFilename/$', 'demo_application.views.echoUploadFilename'),
    url('^postUploadFilename/$', 'demo_application.views.postUploadFilename'),
    # for download files
    url('^downloadFilename/$', 'demo_application.views.downloadFilename'),
)
