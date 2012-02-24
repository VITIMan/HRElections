# -*- coding: utf-8 -*-

import MySQLdb
import os
from MySQLdb.cursors import DictCursor
import datetime

HOST=u'localhost'
USER=u'vitiman_hr_elec'
PASS=u'murcia'
#USER=u'admin'
#PASS=u'P0s0t147369'
DB=u'vitiman_hr_elec'

MAX_VOTES_POINTS = 3
MAX_AVG_POINTS = 5

db=MySQLdb.connect(host=HOST, user=USER, passwd=PASS, db=DB, charset="utf8", init_command = "set names utf8", cursorclass=DictCursor)

cursor=db.cursor()

get_votes='select `stars` from `elections_votes` where `candidate_id`=%s'
get_candidates='select `id` from `elections_candidate`'
set_today="insert into `elections_ranking` (`candidate_id`, `stars`, `avg`, `votes`, `votes_points`, `avg_points`, `ranking`, `published_at`) values (%s, %s, %s, %s, %s, %s, %s, %s)" 
results = []
try:
    cursor.execute(get_candidates)
    candidates=[result['id'] for result in cursor.fetchall()]
    for candidate in candidates:
        cursor.execute(get_votes, (candidate))
        total_votes = cursor.rowcount
        if total_votes==0:
            results.append({'stars':0,
                    'avg':0,
                    'votes':0,
                    'candidate':candidate,
                    })
        else:
            total_stars = sum([result['stars'] for result in cursor.fetchall()])
            avg = float(total_stars)/total_votes
            results.append({'stars':total_stars,'avg':avg, 'votes':total_votes, 'candidate':candidate})
    #cursor.close()

    results_avg = sorted(results, key=lambda k: k['avg'], reverse=True)
    max_avg = results_avg[0]['avg']
    if max_avg>0:
        for result in results_avg:
            result['avg_points']=float((result['avg']*MAX_AVG_POINTS)/max_avg)
    else:
        for result in results_avg:
            result['avg_points']=0
        #Total de votos
    results_avg = sorted(results_avg, key=lambda k: k['votes'], reverse=True)
    max_votes = results_avg[0]['votes']
    if max_votes >0:
        for result in results_avg:
            result['votes_points']=(result['votes']*MAX_VOTES_POINTS)/float(max_votes)
            print "Votes::{0},MAX_VOTES::{1},max_votes::{2},vote_points::{3}".format(result['votes'],MAX_VOTES_POINTS,max_votes,result['votes_points'])
    else:
        for result in results_avg:
            result['votes_points']=0
    results_avg = sorted(results_avg, key=lambda k: k['avg_points']+k['votes_points'], reverse=True)
    #Inserción elections_ranking
    #cursor=db.cursor()
    for ranking, r in enumerate(results_avg):
        #print set_today %  (r['candidate'], r['stars'], r['avg'], r['votes'], r['votes_points'], r['avg_points'], ranking, datetime.datetime.today())
        cursor.execute(set_today, (r['candidate'], r['stars'], r['avg'], r['votes'], r['votes_points'], r['avg_points'], ranking+1,datetime.datetime.now() ))

    cursor.close()
except Exception, e:
    print str(e)
db.close()
