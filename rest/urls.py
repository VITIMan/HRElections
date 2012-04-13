# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from rest.handlers import CandidateHandler
#from piston.authentication import HttpBasicAuthentication

candidate_resource = Resource(handler=CandidateHandler,)

urlpatterns= patterns('',
        url(r'^candidate/(?P<identifier>[^/]+)/', candidate_resource, { 'emitter_format': 'json' }),
        url(r'^candidates/', candidate_resource, { 'emitter_format': 'json' }),
        url(r'^candidates(\.(?P<emitter_format>.+))$', candidate_resource),
)
