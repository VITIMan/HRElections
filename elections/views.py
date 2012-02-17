# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from models import Candidate, Comment, Votes
from forms import LoginForm, RegisterForm, CandidateForm, CommentForm

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect

def index(request):
    pass
    if request.method == 'GET':
        pass
        #Aquí capturaremos id y estrellitas.
    candidates = Candidate.objects.all()
    return render_to_response('index.html', {
        'candidates':candidates,
        }, context_instance=RequestContext(request))

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        print form.is_valid()
        print form.errors
        if form.is_valid():
            # Process the data in form.cleaned_data
            # Salvarlo en USER
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            user=authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/') # Redirect after POST
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
            username = form.cleaned_data['user']
            password = form.cleaned_data['password']
            user=User.objects.create_user(username, username, password)
            user.save()
            return HttpResponseRedirect('/') # Redirect after POST
    else:
        form = RegisterForm() # An unbound form
    return render_to_response('register.html', {
        'form':form,
        }, context_instance=RequestContext(request))

def candidate(request):
    return render_to_response('candidate.html', {}, context_instance=RequestContext(request))
    
@login_required(login_url='/login/')
def publish(request):
    # Ver si está vacío
    published=False   

    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            name = form.cleaned_data['name']
            abbreviation = form.cleaned_data['abbreviation']
            image = form.cleaned_data['image']
            description = form.cleaned_data['description']
            editing = form.cleaned_data['editing']
            if editing != 'NOP':
                candidate=Candidate.objects.get(user=User.objects.get(username__exact=request.user))
                candidate.name = name
                candidate.abbreviation = abbreviation
                candidate.image = image
                candidate.description = description
            else:
                candidate = Candidate(name=name,
                        abbreviation=abbreviation,
                        image=image,
                        description=description,
                        user=User.objects.get(username__exact=request.user),
                        )
            candidate.save()
            published=True
            return HttpResponseRedirect('/publish/') # Redirect after POST
    else:
        try:
            candidate=Candidate.objects.get(user=User.objects.get(username__exact=request.user))
            form = CandidateForm(
                        {'name' : candidate.name,
                            'description' : candidate.description,
                            'abbreviation' : candidate.abbreviation,
                            'image' : candidate.image,
                            'editing': candidate.user.id,
                        }
                    )
        except Candidate.DoesNotExist:
            form = CandidateForm({'editing':'NOP'}) # An unbound form
    return render_to_response('publish.html', {
        'form': form,
        'published': published,
        }, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")
