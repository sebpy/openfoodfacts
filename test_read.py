#!/usr/bin/env python
# -*- coding: utf- -*-

import db_connect as dbc

dbc.DB_CONNECT.execute("select name_categories, link_categories from product_categories")
cate = dbc.DB_CONNECT.fetchall()
print(cate)
