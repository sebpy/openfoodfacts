#!/usr/bin/env python
# -*- coding: utf- -*-
""" Read data from database """

import platform
import os
import db_connect as dbc


class Openfoodfacts:
    """ Class openfoodfacts """

    def __init__(self):
        pass

    def show_categories(self):
        """ Read data from categories_product """

        dbc.DB_CONNECT.execute("select * from product_categories")
        cate = dbc.DB_CONNECT.fetchall()

        print("\nN° |  Categories names\n________________________\n")
        for data in cate:
            print(data[0], "  ", data[1])

        while True:
            print("---------------------------------")
            cate_nb = input("\nN° :")

            try:
                cate_id = int(cate_nb)
                self.read_products_liste(cate_id)

            except ValueError:
                pass

    def read_products_liste(self, id_cate):
        """ Read data from products from id categories and search """

        dbc.DB_CONNECT.execute("select id_product,name_product from products "
                               "where id_categories= '%s'" % id_cate)
        products_list = dbc.DB_CONNECT.fetchall()

        print("N° |  Products names\n________________________\n")
        for products in products_list:
            print(products[0], "  ", products[1])

        while True:
            print("---------------------------------")
            cate_nb = int(input("\nN° :"))

            try:
                product_id = str(cate_nb)
                self.read_product(product_id)

            except ValueError:
                pass

    def read_product(self, id_product):
        """ Read data from products from id categories and search """

        dbc.DB_CONNECT.execute("select * from products where id_product= '%s'" % id_product)
        product_detail = dbc.DB_CONNECT.fetchone()
        dbc.DB_CONNECT.execute("select name_categories from product_categories "
                               "where id_categories='%s'" % product_detail[3])
        category_name = dbc.DB_CONNECT.fetchone()
        dbc.DB_CONNECT.execute("""select name_product, link_product, nutriscore_product
                               from products where id_categories = %s AND nutriscore_product <= '%s'
                               ORDER BY nutriscore_product ASC LIMIT 5""",
                               (product_detail[5], product_detail[3]))
        substitue = dbc.DB_CONNECT.fetchall()

        id_product = product_detail[0]
        save_product = product_detail[8]

        nutriscore_product = {
            0: "A",
            1: "B",
            2: "C",
            3: "D",
            4: "E"
        }
        score = int(product_detail[5])
        print("\n")
        print("Product details:\n------------------")
        print("Product name: ", product_detail[1])
        print("Brand: ", product_detail[2])
        print("Category: ", category_name[0])
        print("Description: ", product_detail[4])
        print("Nutriscore score: ", nutriscore_product[score])
        print("Stores: ", product_detail[6])
        print("Link product: ", product_detail[7])
        print("-----------------------------")
        print("Substitutes:")

        for sub in substitue and range(0, len(substitue)):
            score = int(sub)
            print(''.join(substitue[sub][0]), "| Nutriscore:", nutriscore_product[score])
            print("  ", substitue[sub][1])

        if save_product == "0":
            print("------------------------------")
            save = input("\nDo you want save this product ? (Y/N) \n")
            if save.upper() == "Y":
                dbc.DB_CONNECT.execute("UPDATE products SET save_product='1' "
                                       "WHERE id_product='%s'" % id_product)
                dbc.DB.commit()
                print("Product save!\n\n")
                self.menu()
            else:
                self.menu()
        else:
            print("\n\n")
            self.menu()

    def view_products_saved(self):
        """ View all products saved by user """

        dbc.DB_CONNECT.execute("SELECT id_product, name_product FROM products "
                               "WHERE save_product='1'")
        product_saved = dbc.DB_CONNECT.fetchall()

        nb_saved = len(product_saved)
        if nb_saved == "0":
            print("Product saved is empty")
        else:
            self.clear_console()
            print("""
N°  | Names  """)
            try:
                for datas in product_saved:
                    print(datas[0], ".", datas[1])

                liste_save = int(input("\nN° :"))

                if liste_save > 0:
                    self.read_product(liste_save)

            except ValueError:
                pass

    @staticmethod
    def clear_console():
        """ Clears command line interface """

        if platform.system() == "Windows":
            os.system("cls")
        elif platform.system() == "Linux":
            os.system("clear")

    def clear_saved_products(self):
        """ Delete all saved products """

        dbc.DB_CONNECT.execute("UPDATE products SET save_product='0' WHERE save_product='1'")
        dbc.DB.commit()

        self.clear_console()

    def menu(self):
        """ Print start menu """

        while True:
            dbc.DB_CONNECT.execute("SELECT * FROM products "
                                   "WHERE save_product='1'")
            count_saved = dbc.DB_CONNECT.fetchall()
            print("""Look for a substitute
MENU:
---------------------------------
1. View categories\n2. View products saved""")

            if len(count_saved) >= 1:
                print("3. Clear saved products\n0. Quit")
            else:
                print("0. Quit")

            menu_start = input("\nN° :")

            try:
                menu_int = int(menu_start)
                if menu_int == 0:
                    exit(1)
                elif menu_int == 1:
                    self.show_categories()
                elif menu_int == 2:
                    self.view_products_saved()
                elif menu_int == 3:
                    self.clear_saved_products()
                else:
                    self.clear_console()
            except ValueError:
                pass

    def main(self):
        """ Main function """
        self.menu()


if __name__ == '__main__':
    START = Openfoodfacts()
    START.main()
