from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    # Examples:
    url(r'^$', 'elections.views.index', name='index'),
    url(r'^login/', 'elections.views.login_user', name='login_user'),
    url(r'^register/', 'elections.views.register', name='register'),
    url(r'^publish/', 'elections.views.publish', name='publish'),
    url(r'^candidate/(?P<id>\d+)/$', 'elections.views.candidate', name='candidate'),
    url(r'^candidate/', 'elections.views.candidate', name='candidate'),
    url(r'^logout/','elections.views.logout_user', name='logout_user'),
    # url(r'^hr_elections/', include('hr_elections.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
