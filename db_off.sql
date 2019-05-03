-- Create database OpenFoodFacts whith french datas

-- Encode in utf8
SET NAMES utf8;

-- Delete database if existe and create
DROP DATABASE IF EXISTS `openfoodfacts`;
CREATE DATABASE `openfoodfacts`;

USE openfoodfacts;

-- Create table category
DROP TABLE IF EXISTS product_categories;
CREATE TABLE product_categories (
    id_categories smallint(6) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name_categories VARCHAR(200) CHARACTER SET utf8 NOT NULL,
    link_categories VARCHAR(400) DEFAULT NULL
)ENGINE=InnoDB;

-- Create table product
DROP TABLE IF EXISTS products;
CREATE TABLE products (
    id_product INT(11) UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name_product VARCHAR(250) NOT NULL,
    brand_product VARCHAR(250) DEFAULT NULL,
    id_categories smallint(6) UNSIGNED NOT NULL,
    description_product TEXT DEFAULT NULL,
    nutriscore_product VARCHAR(3) DEFAULT NULL,
    store_product VARCHAR(200) DEFAULT NULL,
    link_product VARCHAR(400) DEFAULT NULL,
    save_product enum('0','1') DEFAULT '0',
    CONSTRAINT id_categories_fk
        FOREIGN KEY (id_categories)
        REFERENCES product_categories(id_categories)
)ENGINE=InnoDB;

ALTER TABLE products CONVERT TO CHARACTER SET utf8;
