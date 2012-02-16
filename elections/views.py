# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

from forms import LoginForm, RegisterForm, CandidateForm, CommentForm

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

def index(request):
    pass
    if request.method == 'GET':
        pass
        #Aquí capturaremos id y estrellitas.

    return render_to_response('index.html', {}, context_instance=RequestContext(request))

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            # Salvarlo en USER
            return HttpResponseRedirect('/thanks/') # Redirect after POST
    else:
        form = LoginForm() # An unbound form

    return render_to_response('login.html', {
        'form': form,
        }, context_instance=RequestContext(request))

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            # Salvarlo en USER
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = RegisterForm() # An unbound form
    return render_to_response('register.html', {
        'form':form,
        }, context_instance=RequestContext(request))

def candidate(request):
    return render_to_response('candidate.html', {}, context_instance=RequestContext(request))
    
@login_required
def publish(request):
    return render_to_response('publish.html', {}, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
def logout(request):
    logout(request)
    return HttpResponseRedirect("/")
