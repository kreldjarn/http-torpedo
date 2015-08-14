# Native
import json

# Framework
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic.base import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from django.core import serializers
from django.http import HttpResponse

# 3rd party
from braces.views import LoginRequiredMixin
import requests
import logfmt

# Models
from torpedo.models import TestRun


###################
#                 #
#    CONSTANTS    #
#                 #
###################

SERVERS = [
	'http://noc2.srv.oz.com:6666'
];

SOURCE_REGIONS = {
    'us-east-1' : 'ec2.us-east-1.amazonaws.com',
    'us-west-2' : 'ec2.us-west-2.amazonaws.com',
    'us-west-1' : 'ec2.us-west-1.amazonaws.com',
    'eu-west-1' : 'ec2.eu-west-1.amazonaws.com',
    'eu-central-1' : 'ec2.eu-central-1.amazonaws.com',
    'ap-southeast-1' : 'ec2.ap-southeast-1.amazonaws.com',
    'ap-southeast-2' : 'ec2.ap-southeast-2.amazonaws.com',
    'ap-northeast-1' : 'ec2.ap-northeast-1.amazonaws.com',
    'sa-east-1' : 'ec2.sa-east-1.amazonaws.com'
}


###############
#             #
#    UTILS    #
#             #
###############

def prune_logs(log):
    # Prune away non-app[web] logs, Isolate JSON part of logs
    log = log.split('\n')
    log = map(lambda l: l.split(': ', 1)[1], filter(lambda l: l[:7] == 'app[web', map(lambda l: l.split(' ', 1)[1], log)))
    # Parse each line into dict
    log = map(lambda l: json.loads(l), log)
    # Prune away requests that are not GET with status 200
    log = filter(lambda l: 'status' in l and
                           l['status'] == 200 and
                           'method' in l and
                           l['method'] == 'GET' and
                           'url' in l, log)

    log = map(lambda l: l['url'], log)

    return log


################
#              #
#    SYSTEM    #
#              #
################

class root(LoginRequiredMixin, View):
    template_name = 'torpedo/root.html'

    def get(self, request):
        return render(request, self.template_name, locals())

class results(LoginRequiredMixin, View):
    template_name = 'torpedo/results.html'

    def get(self, request):
        return render(request, self.template_name, locals())


class upload_log(LoginRequiredMixin, View):
    template_name = 'torpedo/upload_log.html'

    def post(self, request):
        user = request.user
        body = ''
        for chunk in request.FILES['log']:
            body += chunk
        print body
        log = prune_logs(body)
        log = '\x00'.join(log)
        with open('/tmp/LULZ', 'wb+') as dest:
            dest.write(log)

        domain = request.POST.get('domain', 'www.mbl.is')
        cons = request.POST.get('parallel', 0)
        rate = request.POST.get('rate', 0)
        calls = request.POST.get('requests', 0)

    	server = SERVERS[0] # TODO: this.
    	payload = { 'file': open('/tmp/LULZ') }
    	data = { 'calls': calls, 'conns': cons, 'domain': 'www.mbl.is' }
    	r = requests.post(server, data=data, files=payload, timeout=10000)
    	stuff = json.loads(r.content)
        jsonString = r.content

    	x = TestRun()
    	x.json = stuff
    	x.save()

        return render(request, 'torpedo/results.html', locals())

#################
#               #
#   USER MGMT   #
#               #
#################

class register(View):
    def get(self, request):
        args = {}
        args.update(csrf(request))

        args['form'] = UserCreationForm()
        return render_to_response('accounts/register.html', args)

    def post(self, request):
        filled_form = UserCreationForm(request.POST)
        if filled_form.is_valid():
            filled_form.save()
            return HttpResponseRedirect('/success/')
        args = {}
        args.update(csrf(request))
        args['form'] = UserCreationForm()
        args['filled_form'] = filled_form
        return render_to_response('accounts/register.html', args)

class success(View):
    def get(self, request):
        return render_to_response('accounts/success.html')

class login(View):
    def get(self, request):
        next = request.GET.get('next', None)
        return render(request, 'accounts/login.html', locals())

class logout(View):
    def get(self, request):
        auth.logout(request)
        return render_to_response('accounts/logout.html')


def auth_view(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username=username, password=password)

    if user is None:
        return HttpResponseRedirect('/invalid/')
    auth.login(request, user)

    next = request.GET.get('next')
    if next:
        return HttpResponseRedirect(next)
    return HttpResponseRedirect('/')

class logged(View):
    def get(self, request):
        return render_to_response('accounts/logged.html', {'name': request.user.username})

class invalid(View):
    def get(self, request):
        return render_to_response('accounts/invalid.html')

@login_required
def run_test(request):
	server = SERVERS[0] # TODO: this.
	payload = { 'file': open('/tmp/test.txt', 'rb') }
	data = { 'calls': '1', 'conns': '1', 'domain': 'www.mbl.is' }
	r = requests.post(server, data=data, files=payload, timeout=10000)
	stuff = json.loads(r.content)

	x = TestRun()
	x.json = stuff
	x.save()

	return HttpResponse(r.content)
