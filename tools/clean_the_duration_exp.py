#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append("..")

import json

from src.Database import Database


db = Database()

# cmd: update guild2 set last_exp=exp;

ret, msg = db.db_do_update_commond('update guild2 set last_exp=exp;')

print ret
print msg






