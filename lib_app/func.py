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
    data = pd.read_sql(sql_command, conn)
    #print(data.shape)
    data = data.to_dict()
    return data

def pr_menu(ops):
    for index, op in enumerate(ops):
        print("("+str(index)+") " +op)
    return int(input("- "))

def signin():
    loop = 0
    while(loop == 0):
        uname = input("Username: ")
        pswd = input("Password: ")
        res = load_user(uname, pswd)
        print(res)
        print(res["user_pswd"][0])
        if(res["user_pswd"][0] == pswd and res["user_username"][0] == uname):
            print("You're signed in!")
            print()
            sin_menu()
            loop=1
        else:
            ans = input("Thats not right, try again?(y or n) ")
            if(ans == 'n' or ans == 'N'):
                loop = 1

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

def browse_menu():
    e = 0
    while(e == 0):
        ops = ["Sign in to buy book", "More info on specific book", "Main menu"]
        choice = pr_menu(ops)
        if(choice == 0):
            signin()
        elif(choice == 1):
            print(mor_book())
        elif(choice == 2):
            e = 1
        else:
            print("Thats not an option")

def sin_menu():
    #New signed in user menu
    exit = 0
    while(exit == 0):
        ops=["Browse","Search","Cart","Sign out", "Exit"]
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
            print("Signed out!")
        elif(choice == 4):
            exit = 1
            print("Come back soon!")
        else:
            print("Thats not an option")

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
