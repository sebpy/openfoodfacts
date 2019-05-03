#!/usr/bin/env python
# -*- coding: utf- -*-
""" Read data from database """

import platform
import os
import db_connect as dbc


def show_categories():
    """ Read data from categories_product """

    dbc.DB_CONNECT.execute("select * from product_categories")
    cate = dbc.DB_CONNECT.fetchall()

    print("N° |  Categories names\n________________________\n")
    for data in cate:
        print(data[0], "  ", data[1])

    while True:
        print("\nN°  |  Categories")
        print("---------------------------------")
        cate_nb = input("N° :")

        try:
            cate_id = str(cate_nb)
            read_products_liste(cate_id)

        except ValueError:
            clear_console()


def read_products_liste(id_cate):
    """ Read data from products from id categories and search """

    dbc.DB_CONNECT.execute("select id_product,name_product from products "
                           "where id_categories= '%s'" % id_cate)
    products_list = dbc.DB_CONNECT.fetchall()

    print("N° |  Products names\n________________________\n")
    for products in products_list:
        print(products[0], "  ", products[1])

    while True:
        print("\nN°  |  Products")
        print("---------------------------------")
        cate_nb = input("N° :")

        try:
            product_id = str(cate_nb)
            read_product(product_id)

        except ValueError:
            clear_console()


def read_product(id_product):
    """ Read data from products from id categories and search """

    dbc.DB_CONNECT.execute("select * from products where id_product= '%s'" % id_product)
    product_detail = dbc.DB_CONNECT.fetchone()
    dbc.DB_CONNECT.execute("select name_categories from product_categories "
                           "where id_categories='%s'" % product_detail[3])
    category_name = dbc.DB_CONNECT.fetchone()
    dbc.DB_CONNECT.execute("select name_product, link_product, nutriscore_product from products "
                           "where nutriscore_product <= '%s' "
                           "ORDER BY nutriscore_product ASC LIMIT 5" % product_detail[5])
    substitue = dbc.DB_CONNECT.fetchall()

    id_product = product_detail[0]
    name_product = product_detail[1]
    brand_product = product_detail[2]
    category_product = category_name[0]
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
    else:
        nutriscore_product = "E"

    print("\n")
    print("Product details:\n------------------")
    print("Product name: ", name_product)
    print("Brand: ", brand_product)
    print("Category: ", category_product)
    print("Description: ", description_product)
    print("Nutriscore score: ", nutriscore_product)
    print("Stores: ", store_product)
    print("Link product: ", link_product)
    print("-----------------------------")
    print("Substitutes:")

    for sub in substitue and range(0, len(substitue)):
        if substitue[sub][2] == '0':
            nutriscore_sub = "A"
        elif substitue[sub][2] == "1":
            nutriscore_sub = "B"
        elif substitue[sub][2] == "2":
            nutriscore_sub = "C"
        elif substitue[sub][2] == "3":
            nutriscore_sub = "D"
        else:
            nutriscore_sub = "E"

        print(''.join(substitue[sub][0]), "| Nutriscore:", ''.join(nutriscore_sub))
        print("  ", substitue[sub][1])

    if save_product == "0":
        print("------------------------------")
        save = input("Do you want save this product ? (Y/N) ")
        if save.upper() == "Y":
            dbc.DB_CONNECT.execute("UPDATE products SET save_product='1' "
                                   "WHERE id_product='%s'" % id_product)
            dbc.DB.commit()
            print("Product save!\n\n")
            menu()
        else:
            menu()
    else:
        print("\n\n")
        menu()


def view_products_saved():
    """ View all products saved by user """

    dbc.DB_CONNECT.execute("SELECT id_product, name_product FROM products WHERE save_product='1'")
    product_saved = dbc.DB_CONNECT.fetchall()

    nb_saved = len(product_saved)
    if nb_saved == "0":
        print("Product saved is empty")
    else:
        clear_console()
        print("""
N°  | Names  """)
        try:
            for datas in product_saved:
                print(datas[0], ".", datas[1])

            liste_save = input("\nN° :")

            if liste_save > "0":
                read_product(liste_save)

        except ValueError:
            clear_console()


def clear_console():
    """ Clears command line interface """

    if platform.system() == "Windows":
        os.system("cls")
    elif platform.system() == "Linux":
        os.system("clear")


def menu():
    """ Print start menu """

    while True:
        print("""Look for a substitute
MENU:
---------------------------------
1. View categories\n2. View products saved\n3. Quit """)
        menu_start = input("N° :")

        try:
            menu_int = str(menu_start)
            if menu_int == "1":
                show_categories()

            elif menu_int == "2":
                print(view_products_saved())
            elif menu_int == "3":
                break
            else:
                clear_console()
        except ValueError:
            clear_console()


def main():
    """ Main function """
    menu()


if __name__ == '__main__':
    main()
