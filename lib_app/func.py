import psycopg2
import sys, os
import numpy as np
import pandas as pd
import cred_pgsql as cred
import pandas.io.sql as psgql
from random import randint
import current_user as cu

# Set up a connection to the postgres server.
conn_string = "host="+ cred.PGHOST +" port="+ "5432" +" dbname="+ cred.PGDATABASE +" user=" + cred.PGUSER \
+" password="+ cred.PGPASSWORD
conn=psycopg2.connect(conn_string)
print("Connected!")

# Create a cursor object
cursor = conn.cursor()
schema = "allops"

def load_user(uname, pswd):
    table = "user"
    uname = "'"+uname+"'"
    pswd = "'"+pswd+"'"
    sql_command = "select * from {}.{} where user_username = {} and user_pswd = {};".format(str(schema), str(table), uname, pswd)
    data = pd.read_sql(sql_command, conn)
    #print(data)
    data = data.to_dict()
    return data

def num_row(table):
    row_count = "select count(*) from {}.{};".format(str(schema),str(table))
    num_row = pd.read_sql(row_count,conn)
    return int(num_row.at[0,'count']) + 1

def add_user(name,uname,email,pswd):
    table = "user"
    name = "'"+name+"'"
    uname = "'"+uname+"'"
    email = "'"+email+"'"
    pswd = "'"+pswd+"'"
    id = num_row(table)
    sql_command = "insert into {}.{} (user_id, user_name, user_username, user_email, user_pswd) values ({},{},{},{},{});".format(str(schema), str(table),str(id),str(name),str(uname),str(email),str(pswd))
    cursor.execute(sql_command, conn)
    print("You've been added!")

def pr_menu(ops):
    for index, op in enumerate(ops):
        print("("+str(index)+") " +op)
    return int(input("- "))


def signup():
    print("Please enter the following information to create your Look Inna Book account!")
    name = input("Name: ")
    uname = input("Username: ")
    email = input("Email: ")
    pswd = input("Password: ")
    add_user(name, uname, email, pswd)

def browse():
    sql_command = "SELECT * FROM {}.{};".format(str(schema), "book")
    #print (sql_command)
    # Load the data
    data = pd.read_sql(sql_command, conn)
    data = data.to_dict()
    return data


def mor_book():
    name = input("Name of book: ")
    name = "'"+name+"'"
    sql_command = "SELECT * FROM {}.{} where bk_name = {};".format(str(schema), "book", str(name))
    data = pd.read_sql(sql_command, conn)
    #print(data)
    return data

"""
def load_data(schema, table):

    sql_command = "SELECT * FROM {}.{};".format(str(schema), str(table))
    print (sql_command)

    # Load the data
    data = pd.read_sql(sql_command, conn)

    print(data.shape)
    return (data)
"""
