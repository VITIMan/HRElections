from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

#elections_patterns = patterns('elections.views',
#
#    (r'^$', 'index'),
#    (r'^login/', 'login_user'),
#    (r'^register/','register'),
#    (r'^publish/', 'publish'),
#    (r'^candidate/(?P<id>\d+)/$', 'candidate'),
#    (r'^candidate/', 'candidate'),
#    (r'^logout/','logout_user'),
#)

urlpatterns = patterns('',
    
    # Examples:

    url(r'^$', 'elections.views.index', name='index'),
    url(r'^(?i)login/', 'elections.views.login_user', name='login_user'),
    url(r'^(?i)register/', 'elections.views.register', name='register'),
    url(r'^(?i)publish/', 'elections.views.publish', name='publish'),
    url(r'^(?i)candidate/(?P<id>\d+)', 'elections.views.candidate', name='candidate'),
    #url(r'^candidate/', 'elections.views.candidate', name='candidate'),
    url(r'^(?i)logout/','elections.views.logout_user', name='logout_user'),
    #url(r'^$', direct_to_template, {'template': 'soon.html'}),
    
    # url(r'^hr_elections/', include('hr_elections.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    #url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^(?i)admin/', include(admin.site.urls)),
)
