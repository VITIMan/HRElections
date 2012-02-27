# -*- coding: utf-8 -*-
from django.contrib.syndication.views import Feed
from models import Comment, Candidate

class CommentFeed(Feed):
    def items(self):
        return Comment.objects.order_by('-published_at')[:10]

    def item_title(self, item):
        return "Comentario de {0} en {1}".format(item.name, item.candidate.name )

    def item_description(self, item):
        return item.text

    def link(self, item):
        return '/candidate/{0}'.format(item.candidate.id)

class CandidateFeed(Feed):
    def items(self):
        return Candidate.objects.order_by('-published_at')[:50]

    def item_title(self, item):
        return item.name

    def item_description(self, item):
        return item.description

    def link(self, item):
        return '/candidate/{0}'.format(item.id)
