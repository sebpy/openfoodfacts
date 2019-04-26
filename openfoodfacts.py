#!/usr/bin/env python
# -*- coding: utf- -*-
""" Read data from database """


import db_connect as dbc


def show_categories():
    """ Read data from categories_product """

    dbc.DB_CONNECT.execute("select * from product_categories")
    cate = dbc.DB_CONNECT.fetchall()

    i = 0
    print("N° |  Categories names\n________________________\n")
    for data in cate:
        print(cate[i][0], "  ", cate[i][1])
        i += 1

    return data


def read_categories(id_cate):
    """ Read data from categories_product with id """

    dbc.DB_CONNECT.execute("select name_categories from product_categories where id_categories= '%s'" % id_cate)
    cate = dbc.DB_CONNECT.fetchone()
    print(cate)
    #return cate


def read_products():
    """ Read data from products from id categories and search """
    pass


def save_product():
    """ Save product for current user """
    pass


def main():
    show_categories()
    print("\n\nEnter the category number")
    enter_categories = input("N° :")
    try:
        value = int(enter_categories)
        if value > 0:
            read_categories(value)
        else:
            print("You must enter number")
    except ValueError:
        print("No.. input string is not a number. It's a string")



    #read_categories(23)


if __name__ == '__main__':
    main()
