#!/usr/bin/env python
# -*- coding: utf- -*-

""" Create database with the OpenFoodFacts API"""

#Import modules
import json
import MySQLdb
import requests as rq

import db_connect as dbc


#Constants
DB_FILE = 'db_off.sql'
OFF_CAT = 'https://fr.openfoodfacts.org/categories.json'
OFF_URL = 'https://world.openfoodfacts.org/country/france'

DB = MySQLdb.connect(host=dbc.mysql['host'], user=dbc.mysql['user'], passwd=dbc.mysql['passwd'],
                     use_unicode=True, charset='utf8')

DB_CONNECT = DB.cursor()


def get_data_api(url):
    """" Get all data from api OpenFoodFacts """
    data = rq.get(url)
    return data.json()


def main():
    view = get_data_api(OFF_CAT)
    print(view)


if __name__ == "__main__":
    main()

