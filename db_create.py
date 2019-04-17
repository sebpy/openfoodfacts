#!/usr/bin/env python
# -*- coding: utf- -*-

""" Create database with the OpenFoodFacts API"""

# Import modules
import json
import math
import requests as rq

import db_connect as dbc


# Constants
DB_FILE = 'db_off.sql'
OFF_CAT = 'https://fr.openfoodfacts.org/categories.json'
OFF_URL = 'https://fr.openfoodfacts.org'


def get_data_api(url):
    """" Get all data from api OpenFoodFacts """
    data = rq.get(url)
    return data.json()


def categories_table(url):
    """ Get category from json data of openfoodfacts and insert in table categories"""

    get_data = get_data_api(url)
    for data in get_data["tags"]:
        if data["products"] > 150 and 'en:' in data['id']:

            dbc.DB_CONNECT.execute("INSERT INTO product_categories values ('0', %s, %s)", (data["name"], data["url"]))
            dbc.DB.commit()

    print("Data add in table categories_product")
    dbc.DB.close()


def products_table(url_category):

    url_json = str(''.join(url_category))
    get_data = get_data_api(url_json + ".json")
    nb_pages = int(math.ceil(get_data["count"] / get_data["page_size"]))

    data = []

    for page in range(0, nb_pages):
        categories_pages = url_json + "/" + str(page+1) + ".json"
        get_data_categories = get_data_api(categories_pages)

        for product in get_data_categories["products"]:
            try:
                product_mane = product["product_name_fr"]
            except KeyError:
                pass

            try:
                product_brand = product["product_name_fr"]
            except KeyError:
                product_brand = "N/A"

            try:
                product_category = product["categories"]
            except KeyError:
                pass

            #data.append((product_mane, product_brand, product_category))

            print(product_mane, product_brand, product_category)

def main():
    dbc.DB_CONNECT.execute("select link_categories from product_categories")
    categories_product = dbc.DB_CONNECT.fetchall()

    for data in categories_product:
        products_table(data)


if __name__ == "__main__":
    main()

