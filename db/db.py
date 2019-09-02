#!/usr/bin/python3


import mysql.connector as mysql
from configparser import ConfigParser


def connect_to_mysql(filename='config.ini', section='mysql'):
    parser = ConfigParser()
    parser.read(filename)

    db = {}
    items = parser.items(section)
    for item in items:
        db[item[0]] = item[1]

    connection = mysql.connect(**db)
    return connection


def create_db(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS onliner_rent")
    cursor.execute("USE onliner_rent")
    connection.commit()


def use_db(connection, db_name):
    cursor = connection.cursor()
    cursor.execute("USE %s" % db_name)
    connection.commit()


def create_table(connection):
    cursor = connection.cursor()
    sql = """CREATE TABLE IF NOT EXISTS `apartments` (
    `id` INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    `hash` LONGTEXT,
    `url` LONGTEXT
    )"""
    cursor.execute(sql)
    connection.commit()


if __name__ == '__main__':
    connection = connect_to_mysql()
    create_db(connection)
    create_table(connection)
