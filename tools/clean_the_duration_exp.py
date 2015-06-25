#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

import json

from src.Database import Database


db = Database()

ret, msg,data = db.db_do_select_commond('select id,account from player2;')

print ret
print msg

for one in data:
    print "id:%s, account:%s" %(one[0],one[1])




