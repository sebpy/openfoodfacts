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


def read_products_liste(id_cate):
    """ Read data from products from id categories and search """

    dbc.DB_CONNECT.execute("select id_product, name_product from products where category_product= '%s'" % id_cate)
    products_list = dbc.DB_CONNECT.fetchall()

    i = 0
    print("N° |  Products names\n________________________\n")
    for products in products_list:
        print(products_list[i][0], "  ", products_list[i][1])
        i += 1

    return products


def read_product(id_product):
    """ Read data from products from id categories and search """

    dbc.DB_CONNECT.execute("select * from products where id_product= '%s'" % id_product)
    product_detail = dbc.DB_CONNECT.fetchone()

    name_product = product_detail[1]
    brand_product = product_detail[2]
    category_product = product_detail[3]
    description_product = product_detail[4]
    nutriscore_product = product_detail[5]
    store_product = product_detail[6]
    link_product = product_detail[7]
    save_product = product_detail[8]

    if nutriscore_product == '0':
        nutriscore_product = "A"
    elif nutriscore_product == "1":
        nutriscore_product = "B"
    elif nutriscore_product == "2":
        nutriscore_product = "C"
    elif nutriscore_product == "3":
        nutriscore_product = "D"
    elif nutriscore_product == "4":
        nutriscore_product = "E"
    else:
        nutriscore_product = "N/A"

    print("\n")
    print("Product details:\n------------------")
    print("Product name: ", name_product)
    print("Brand: ", brand_product)
    print("Category: ", category_product)
    print("Description: ", description_product)
    print("Nutriscore score: ", nutriscore_product)
    print("Stores: ", store_product)
    print("Link product: ", link_product)


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
            read_products_liste(value)
            enter_product = input("Enter product number: ")
            try:
                value = int(enter_product)
                if value > 0:
                    read_product(value)
                else:
                    print("You must enter number")
            except ValueError:
                print("No.. input string is not a number. It's a string")
        else:
            print("You must enter number")
    except ValueError:
        print("No.. input string is not a number. It's a string")


if __name__ == '__main__':
    main()
