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

# 3rd party
from braces.views import LoginRequiredMixin


##############
#            #
#    VARS    #
#            #
##############

source_regions = {
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

################
#              #
#    SYSTEM    #
#              #
################

class root(LoginRequiredMixin, View):
    template_name = 'torpedo/root.html'

    def get(self, request):
        return render(request, self.template_name, locals())


class upload_log(LoginRequiredMixin, View):
    template_name = 'torpedo/upload_log.html'

    def post(self, request):
        user = request.POST.get('user')
        print(user)
        print(source_regions)
        return render(request, self.template_name, locals())




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