from django.conf.urls import include, url
from django.contrib import admin
from torpedo.views import *
from django.http import HttpResponse

from torpedo.models import TestRun

import json
import requests

SERVERS = [
	'http://noc2.srv.oz.com:6666'
];

def run_test(args):
	server = SERVERS[0] # TODO: this.
	payload = { 'file': open('/tmp/test.txt', 'rb') }
	data = { 'calls': '1', 'conns': '1', 'domain': 'www.mbl.is' }
	r = requests.post(server, data=data, files=payload, timeout=10000)
	stuff = json.loads(r.content)

	x = TestRun()
	x.json = stuff
	x.save()

	return HttpResponse(r.content)

urlpatterns = [
	# LOGIC
	url(r'^$', root.as_view()),
    url(r'^results$', results.as_view()),
	url(r'^upload-log/$', upload_log.as_view(), name='upload_log'),
	url(r'^run-test/$', run_test),



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
