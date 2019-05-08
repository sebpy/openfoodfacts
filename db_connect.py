#!/usr/bin/env python
# -*- coding: utf- -*-

""" Connect to database """

import MySQLdb


mysql = {
    'host': 'localhost',
    'user': 'off',
    'passwd': 'projet_5',
    'db': 'openfoodfacts'
}

DB = MySQLdb.connect(host=mysql['host'], user=mysql['user'], passwd=mysql['passwd'],
                     db=mysql['db'], use_unicode=True, charset='utf8')
DB_CONNECT = DB.cursor()

