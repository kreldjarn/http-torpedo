from django.conf.urls import include, url
from django.contrib import admin
from torpedo.views import *

urlpatterns = [
	url(r'^$', root.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^login/$', 'django.contrib.auth.views.login'),
    #url(r'^logout/$', 'django.contrib.auth.views.logout'),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^account/login/$', login.as_view(), name='login'),
    url(r'^account/authenticate/$', auth_view, name='authenticate'),
    url(r'^account/logout/$', logout.as_view(), name='logout'),
    url(r'^account/logged/$', logged.as_view()),
    url(r'^account/invalid/$', invalid.as_view()),

    url(r'^account/register/$', register.as_view(), name='register'),
    url(r'^account/success/$', success.as_view()),
]
