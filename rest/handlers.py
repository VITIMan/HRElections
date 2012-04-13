#-*- coding: utf-8 -*-
from piston.handler import BaseHandler
from piston.utils import rc, throttle
from elections.models import Candidate

"""
Just a Simple piston testing in this project
"""

class CandidateHandler(BaseHandler):
    """
    retrieve candidate information
    """
    allowed_methods = ('GET',)
    model = Candidate
    fields = ('name', 'abbreviation', 'description', 'image', 'published_at',('user', ('username', )))
    #exclude = ('user',)

    #@throttle(5, 10*60) # allow 5 times in 10 minutes
    def read(self, request, identifier=None):
        """
        Returns a single post if identifier is given.
        Otherwise returns a subset
        """
        candidate = Candidate.objects
        if identifier:
            try:
                return candidate.get(pk=identifier)
            except Candidate.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return candidate.all()

#class AllCandidatesHandler(BaseHandler):
#    """
#    Retrieves all candidates
#    """
#    allowed_methods = ('GET',)
