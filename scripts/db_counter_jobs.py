# -*- coding: utf-8 -*-

import MySQLdb
import os
from MySQLdb.cursors import DictCursor

HOST=u'localhost'
USER=u'admin'
PASS=u'P0s0t147369'


dbname = u'posottrabajos_'
countries = [u'de_de',
        u'en_ca',
        u'en_gb',
        u'en_in',
        u'en_us',
        u'es_ar',
        u'es_es',
        u'es_mx',
        u'fr_fr',
        u'it_it',
        u'pt_pt',
        u'pt_br',
        ]

table_definition = u"""
CREATE TABLE IF NOT EXISTS `total_classifieds` (
    `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
    `country` varchar(255) DEFAULT NULL,
    `q` int(10) DEFAULT 0,
    PRIMARY KEY (`id`),
    UNIQUE(`country`)
    ) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='utf8_general_ci'
"""

query="select count(id) as counter from classifieds"

counter={}

for country in countries:
    db=MySQLdb.connect(host=HOST, user=USER, passwd=PASS, db=dbname + country, charset="utf8", init_command = "set names utf8", cursorclass=DictCursor)
    cursor=db.cursor()
    try:
        cursor.execute(query)
        counter[country]=cursor.fetchone()['counter']
    except Exception, e:
        pass
        #print str(e)

    #cursor.close()
    db.close()


query_insert=u"INSERT IGNORE INTO `total_classifieds` (`country`) VALUES (%s)"
query_update=u"UPDATE `total_classifieds` SET `q`=%s WHERE `country`=%s"
db=MySQLdb.connect(host=HOST, user=USER, passwd=PASS, db=u'posottrabajos_es_es', charset="utf8", init_command = "set names utf8", cursorclass=DictCursor)
cursor=db.cursor()
try:
    cursor.execute("drop table if exists total_classifieds;")
    cursor.execute(table_definition)
except Exception, e:
    pass
    #print str(e)
db.close()

#.--------------
db=MySQLdb.connect(host=HOST, user=USER, passwd=PASS, db=u'posottrabajos_es_es', charset="utf8", init_command = "set names utf8", cursorclass=DictCursor)
cursor=db.cursor()
for country in countries:
    try:
        cursor.execute(query_insert, country)
        cursor.execute(query_update ,(counter[country], country))
    except Exception, e:
        pass
        #print str(e)
cursor.close()
db.close()

os.system("/var/www/sphinx/bin/indexer --config /home/trabajo/scripts/posot_index/jobs_sphinx_myisam.conf counter_jobs --rotate")

os.system("chown -R apache:apache /var/www/sphinx/var/data/trabajoposot")
