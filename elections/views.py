# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from models import Candidate, Comment, Votes, Ranking
from forms import LoginForm, RegisterForm, CandidateForm, CommentForm

from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
import datetime
from django.db.models import Max

def index(request):
    print 0/0
    already_voted = 0
    vote_well = True
    vote_success = False
    id = request.GET.get('id', 0)
    stars = request.GET.get('v', 0)
    registered = request.GET.get('r','false') 
    if registered == 'true':
        registered = True
    else:
        registered = False
    if id!=0 and stars!=0:
        try:
            if int(stars) not in range(1,6):
                raise ValueError()
            #Aquí capturaremos id y estrellitas.
            ip = _get_client_ip(request)
            candidate = Candidate.objects.get(id=id)
            votes_today=Votes.objects.filter(
                    candidate = candidate
                    ,ip=ip,
                    voted_at__gte = datetime.date.today()) 
            if len(votes_today) == 0:
                vote = Votes(candidate=candidate,
                        stars=stars,
                        ip=ip)

                vote.save()
                vote_success = True
            else:
                already_voted = candidate.id
        except ValueError:
            vote_well = False  
        except Candidate.DoesNotExist:
            vote_well = False
    #candidates = Candidate.objects.all()
    p=Ranking.objects.all().aggregate(Max('published_at')) 
    #ranking=Ranking.objects.all().order_by('published_at')[:Candidate.objects.count()]
    ranking=Ranking.objects.filter(published_at=p['published_at__max'])
    candidates = [rank.candidate for rank in ranking]
    no_rank_candidates = Candidate.objects.exclude(pk__in=[c.pk for c in candidates])
    candidates +=no_rank_candidates
    #print no_rank_candidates
    #for rank in ranking:
    #    print rank.ranking
    #    print rank.candidate
    return render_to_response('index.html', {
        'candidates':candidates,
        'registered':registered,
        'already_voted':already_voted,
        'vote_well': vote_well,
        'vote_success':vote_success,
        }, context_instance=RequestContext(request))

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
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
            return HttpResponseRedirect('/?r=true') # Redirect after POST
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
    new = False
    deleted = False
    delete = request.GET.get('d', 'n')
    if delete == 'y':
        try:
            candidate=Candidate.objects.get(user=User.objects.get(username__exact=request.user))
            candidate.delete()
            deleted = True
        except Candidate.DoesNotExist:
            pass
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
                # Edit candidate
                candidate=Candidate.objects.get(user=User.objects.get(username__exact=request.user))
                candidate.name = name
                candidate.abbreviation = abbreviation
                candidate.image = image
                candidate.description = description
            else:
                # New Candidate
                candidate = Candidate(name=name,
                        abbreviation=abbreviation,
                        image=image,
                        description=description,
                        user=User.objects.get(username__exact=request.user),
                        )

            candidate.save()
            published=True
    else:
        # If candidate exist, let's populate the form
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
            new = True
            form = CandidateForm({'editing':'NOP'})
    return render_to_response('publish.html', {
        'form': form,
        'published': published,
        'new' : new,
        'deleted': deleted,
        }, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def _get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def candidate(request, id):
    
    try:
        candidate=get_object_or_404(Candidate, pk=id)
        comments = Comment.objects.filter(candidate=candidate).order_by('-published_at')
    except Candidate.DoesNotExist:
        pass #404

    comment_mucho = False
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            text = form.cleaned_data['text']
            ip = _get_client_ip(request)

            comments_now = Comment.objects.filter(
                    candidate=candidate,
                    ip=ip,
                    published_at__gte=datetime.datetime.today() - datetime.timedelta(minutes=5) # 5 comment in 5 minutes
                    )
            print len(comments_now)
            if len(comments_now)<5: 
                comment = Comment(candidate=candidate,
                    name = name,
                    text = text,
                    ip = ip,
                    )
                comment.save()
            else:
                comment_mucho = True
            form = CommentForm()   
    else: 
        form = CommentForm()
    return render_to_response('candidate.html', {
        'candidate':candidate,
        'comments':comments,
        'full_path': request.build_absolute_uri(),
        'form': form,
        'comment_mucho': comment_mucho,
        }, context_instance=RequestContext(request))
