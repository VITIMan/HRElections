# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from models import Comment, Candidate

class CommentFeed(Feed):
    """
    Feed for lastest comments published. All comments. 
    Make particulary for each candidate is trivial.
    """
    title = 'HRElections::Últimos comentarios'
    link = ''
    description = 'Últimos comentarios publicados'

    def get_object(self, request):
        c= Comment.objects.order_by('-published_at')[:50]
        return Comment.objects.order_by('-published_at')[:50]
    def items(self, obj):
        return obj

    def item_title(self, item):
        return u"Comentario de {0} en {1}".format(item.name, item.candidate.name )

    def item_description(self, item):
        return item.text

    def item_link(self, item):
        return '/candidate/{0}'.format(item.candidate.pk)

class CandidateFeed(Feed):
    """
    Feed for lastest candidates published.
    """
    title = 'HRElections::Últimos candidatos'
    link = ''
    description=u'Últimas candidaturas publicadas'

    def link(self, obj):
        return '/'

    def get_object(self, request):
        return Candidate.objects.order_by('-published_at')[:5]

    def items(self, obj):
        return obj 

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        return '/candidate/{0}'.format(item.id)

    def item_pubdate(self, item):
        return item.published_at

