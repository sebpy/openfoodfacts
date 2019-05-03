#!/usr/bin/env python
# -*- coding: utf- -*-

""" Create database with the OpenFoodFacts API"""

# Import modules
import sys
import re
import math
from tqdm import tqdm
import requests as rq

import db_connect as dbc


class database:
    """ Class for create database """

    def __init__(self):
        self.db_file = 'db_off.sql'
        self.off_cat = 'https://fr.openfoodfacts.org/categories.json'
        self.off_url = 'https://fr.openfoodfacts.org'

    def exec_sql_file(self, sql_file):
        """ Create database """

        print("--- Creating database ---")
        print("1. Executing SQL script file: '%s'" % (sql_file))
        statement = ""

        for line in open(sql_file):
            if re.match(r'--', line):  # ignore sql comment lines
                continue
            if not re.search(r'[^-;]+;', line):  # keep appending lines that don't end in ';'
                statement = statement + line
            else:  # when you get a line ending in ';' then exec statement and reset for next statement
                statement = statement + line
                #print "\n\n[DEBUG] Executing SQL statement:\n%s" % (statement)
                try:
                    dbc.DB_CONNECT.execute(statement)
                except dbc.DB.Error as err:
                    print("\n[WARN] MySQLError during execute statement "
                          "\n\tArgs: '%s'" % (str(err.args)))

                statement = ""
        print("\n   [Info] Database Create")

    def get_data_api(self, url):
        """" Get all data from api OpenFoodFacts """
        data = rq.get(url)
        return data.json()

    def categories_table(self, url):
        """ Get category from json data of openfoodfacts and insert in table categories"""

        get_data = self.get_data_api(url)
        for data in get_data["tags"]:

            if data["products"] in range(55, 60) and 'en:' in data['id']:
                dbc.DB_CONNECT.execute("INSERT INTO product_categories "
                                       "values ('0', %s, %s)", (data["name"], data["url"]))
                dbc.DB.commit()

        print("   [Info] Data add in table categories_product")

    def products_table(self, id_categories, url_categories):
        """ Get all products from categories and insert into database """

        url_json = str(''.join(url_categories))
        get_data = self.get_data_api(url_json + ".json")
        nb_pages = int(math.ceil(get_data["count"] / get_data["page_size"]))

        for page in range(0, nb_pages):
            categories_pages = url_json + "/" + str(page+1) + ".json"
            get_data_categories = self.get_data_api(categories_pages)

            for product in get_data_categories["products"]:

                try:
                    product_mane = product["product_name_fr"]
                except KeyError:
                    product_mane = "N/A"

                try:
                    product_brand = product["brands"]
                except KeyError:
                    product_brand = "N/A"

                try:
                    product_description = str(product["ingredients_text_fr"])
                except KeyError:
                    product_description = "N/A"

                try:
                    if product["nutrition_grade_fr"] == 'a':
                        product_nutriscore = "0"
                    elif product["nutrition_grade_fr"] == 'b':
                        product_nutriscore = "1"
                    elif product["nutrition_grade_fr"] == 'c':
                        product_nutriscore = "2"
                    elif product["nutrition_grade_fr"] == 'd':
                        product_nutriscore = "3"
                    elif product["nutrition_grade_fr"] == 'e':
                        product_nutriscore = "4"
                    else:
                        product_nutriscore = "4"

                except KeyError:
                    product_nutriscore = "e"

                try:
                    if not product["stores"]:
                        product_store = "N/A"
                    else:
                        product_store = product["stores"]
                except KeyError:
                    product_store = "N/A"

                try:
                    product_link = product["url"]
                except KeyError:
                    product_link = "N/A"

                try:
                    dbc.DB_CONNECT.execute("INSERT INTO products "
                                           "values ('0', %s, %s, %s, %s, %s, %s, %s, "
                                           "'0')",
                                           (product_mane, product_brand, id_categories,
                                            product_description, product_nutriscore,
                                            product_store, product_link))
                    dbc.DB.commit()

                except dbc.DB.Error as err:
                    print("Error %s: %s" % (err.args[0], err.args[1]))
                    sys.exit(1)

                # Clean db
                try:
                    # DELETE duplicate name and no name entry
                    dbc.DB_CONNECT.execute("DELETE FROM `products` WHERE name_product='N/A'")
                    dbc.DB_CONNECT.execute("DELETE FROM `products` WHERE id_product NOT IN "
                                           "(SELECT id_product FROM (SELECT max(id_product) id_product "
                                           "FROM products GROUP BY name_product) as doublon);")
                    dbc.DB.commit()

                except dbc.DB.Error as err:
                    print("Error %s: %s" % (err.args[0], err.args[1]))
                    sys.exit(1)

    def main(self):
        """ Function main """

        self.exec_sql_file(self.db_file)
        self.categories_table(self.off_cat)

        dbc.DB_CONNECT.execute("select id_categories, link_categories from product_categories")
        categories_product = dbc.DB_CONNECT.fetchall()

        print("\n 2. Add data in table products_table")
        print("   Please wait...")

        pbar = tqdm(total=1140, ncols=100)

        for data in categories_product:
            id_cate = data[0]
            link_cate = data[1]
            self.products_table(id_cate, link_cate)
            pbar.update(20)
        pbar.close()
        dbc.DB.close()
        print("   [Info] Dump data is ok!")


if __name__ == "__main__":
    database.main()
