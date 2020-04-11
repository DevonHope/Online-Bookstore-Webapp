import psycopg2
import sys, os
import numpy as np
import pandas as pd
import cred_pgsql as cred
import pandas.io.sql as psgql
from random import randint

# Set up a connection to the postgres server.
conn_string = "host="+ cred.PGHOST +" port="+ "5432" +" dbname="+ cred.PGDATABASE +" user=" + cred.PGUSER \
+" password="+ cred.PGPASSWORD
conn=psycopg2.connect(conn_string)
print("Connected!")

# Create a cursor object
cursor = conn.cursor()
schema = "allops"

def getRowNum():
    table = "user"
    row_count = "select count(*) from {}.{};".format(str(schema),str(table))
    num_row = pd.read_sql(row_count,conn)
    print(num_row)
    print(num_row.at[0,'count'])

def load_user(uname, pswd):
    table = "user"
    uname = "'"+uname+"'"
    pswd = "'"+pswd+"'"
    sql_command = "select * from {}.{} where user_username = {} and user_pswd = {};".format(str(schema), str(table), uname, pswd)
    data = pd.read_sql(sql_command, conn)
    #print(data.shape)
    data = data.to_dict()
    return data

def add_user(name,uname,email,pswd):
    table = "user"
    name = "'"+name+"'"
    uname = "'"+uname+"'"
    email = "'"+email+"'"
    pswd = "'"+pswd+"'"
    row_count = "select count(*) from {}.{};".format(str(schema),str(table))
    num_row = pd.read_sql(row_count,conn)
    id = int(num_row.at[0,'count']) + 1
    sql_command = "insert into {}.{} (user_id, user_name, user_username, user_email, user_pswd) values ({},{},{},{},{});".format(str(schema), str(table),id,name,uname,email,pswd)
    data = pd.read_sql(sql_command, conn)
    #print(data.shape)
    data = data.to_dict()
    return data

def rand_n(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def pr_menu(ops):
    for index, op in enumerate(ops):
        print("("+str(index)+") " +op)
    return int(input("- "))

def signin():
    uname = input("Username: ")
    pswd = input("Password: ")
    res = load_user(uname, pswd)
    if(not res):
        return 0
    else:
        return 1

def signup():
    print("Please enter the following information to create your Look Inna Book account!")
    name = input("Name: ")
    uname = input("Username: ")
    email = input("Email: ")
    pswd = input("Password: ")
    res = add_user(name, uname, email, pswd)
    if(res):
        return 1
    else:
        return 0

def browse():
    sql_command = "SELECT * FROM {}.{};".format(str(schema), "book")
    #print (sql_command)
    # Load the data
    data = pd.read_sql(sql_command, conn)
    data = data.to_dict()
    return data

def sin_menu():
    #New signed in user menu
    exit = 0
    while(exit == 0):
        ops=["Browse","Search","Cart", "Exit"]
        print("Please select an option from the list below by number")
        choice = pr_menu(ops)
        if(choice == 0):
            print(browse())
        elif(choice == 1):
            search()
        elif(choice == 2):
            cart()
        elif(choice == 3):
            exit = 1
            print("Come back soon!")
        elif(choice > len(ops)-1):
            print("Thats not an option")

def mor_book():
    name = input("Name of book: ")
    name = "'"+name+"'"
    sql_command = "SELECT * FROM {}.{} where bk_name = {};".format(str(schema), "book", str(name))
    data = pd.read_sql(sql_command, conn)
    #print(data)
    return data
