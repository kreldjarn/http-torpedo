from django.conf.urls import include, url
from django.contrib import admin
from torpedo.views import *

urlpatterns = [
	# LOGIC
	url(r'^$', root.as_view()),
    url(r'^results$', results.as_view()),
	url(r'^upload-log/$', upload_log.as_view(), name='upload_log'),

	# SYSTEM
    url(r'^admin/', include(admin.site.urls)),

    url(r'^login/$', login.as_view(), name='login'),
    url(r'^authenticate/$', auth_view, name='authenticate'),
    url(r'^logout/$', logout.as_view(), name='logout'),
    url(r'^logged/$', logged.as_view()),
    url(r'^invalid/$', invalid.as_view()),

    url(r'^register/$', register.as_view(), name='register'),
    url(r'^success/$', success.as_view(), name='success'),
]
