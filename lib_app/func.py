import psycopg2
import sys, os
import numpy as np
import pandas as pd
import cred_pgsql as cred
import pandas.io.sql as psgql
from random import randint
import current_user as cu
import pprint
import string

# Set up a connection to the postgres server.
conn_string = "host="+ cred.PGHOST +" port="+ "5432" +" dbname="+ cred.PGDATABASE +" user=" + cred.PGUSER \
+" password="+ cred.PGPASSWORD
conn=psycopg2.connect(conn_string)
print("Connected!")

# Create a cursor object
cursor = conn.cursor()
schema = "allops"

def insert_db(sql_command):
    try:
        cursor.execute(sql_command, conn)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def load_db(sql_command):
    res = None
    try:
        data = pd.read_sql(sql_command, conn)
        res = data.to_dict()
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    return res

def load_user(uname, pswd):
    table = "user"
    uname = "'"+uname+"'"
    pswd = "'"+pswd+"'"
    sql_command = "select * from {}.{} where user_username = {} and user_pswd = {};".format(str(schema), str(table), uname, pswd)
    data = load_db(sql_command)
    return data

def update_cart(user):
    table="checkout"
    getid = "select * from {}.{} where ch_userid = {};".format(str(schema),str(table),str(user.getID()))
    res = load_db(getid)
    names = user.getCheck().keys()
    #print(names)
    price = user.getCheck().values()
    #print(price)
    book = []
    for n in names:
        for p in price:
            book.append(""+n+":"+str(p))
        #print(n)
    book = str( book)
    book = book.replace('[', '{').replace(']', '}').replace('\'', '\"')
    #query = '''update "aTable" SET "Test" = '%s\'''' %(list)
    if(not res['ch_userid']):
        con = "insert into {}.{} values ({},{},{},{});".format(str(schema),str(table),str(user.getID()), str(user.getBA()), str(user.getSA()),book)
    else:
        con = "update {}.{} set ch_books = {};".format(str(schema),str(table), book)
    insert_db(con)
    print("Cart added to DB")

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
    insert_db(sql_command)
    print("You've been added!")

def pr_menu(ops):
    res = None
    for index, op in enumerate(ops):
        print("("+str(index)+") " +op)
    try:
        res = int(input("- "))
    except ValueError:
        print("Thats not an option")
        print()
    except KeyboardInterrupt:
        print("Come again!")
        sys.exit()
    return res


def signup():
    loop = 0
    while(not loop):
        print("Enter 'e' to exit")
        print("Please enter the following information to create your Look Inna Book account!")
        name = input("Name: ")
        if(name == 'e'):
            loop = 1
        uname = input("Username: ")
        if(uname == 'e' ):
            loop = 1
        email = input("Email: ")
        if(email == 'e'):
            loop = 1
        pswd = input("Password: ")
        if(pswd == 'e'):
            loop = 1
        else:
            add_user(name, uname, email, pswd)
            loop=1

def browse():
    sql_command = "SELECT * FROM {}.{};".format(str(schema), "book")
    # Load the data
    data = load_db(sql_command)
    if(not data):
        print("Sorry! No books to be found here!")
        print("Try another day!")
        print()
    print("Books on hand:")
    d = {"Name" : "Price"}
    p = {}
    pprint.pprint(d)
    for i in data["bk_name"]:
        pr = "$" + str(data["bk_price"][i])
        p.update({data["bk_name"][i] : pr})

    pprint.pprint(p)

def addCart(user):
    loop = 0
    while( not loop):
        print("Enter 'e' to exit")
        book = input("Enter the name of the book: ")
        if(book == 'e'):
            loop = 1
        book = string.capwords(str(book))
        book = "'"+book+"'"
        #print(book)
        if(book):
            sql_command = "SELECT * FROM {}.{} where bk_name = {};".format(str(schema), "book", str(book))
            res = load_db(sql_command)
            if not res["bk_name"]:
                print("That is not a book")
                ans = input("Do you want to add another book?(y or n) ")
                if(ans == 'n' or ans == 'N'):
                    loop = 1
                    print()
            else:
                #print(res)
                user.setCheckout(res)
                loop = 1

    return user

def cart(user):
    cart_books = user.getCheck()
    #print(cart_books)
    print()
    print("CART:")
    for b in cart_books:
        print(b)
    print()

def mor_book():
    loop = 0
    while(not loop):
        print("Enter 'e' to exit")
        name = input("Name of book: ")
        if(name == 'e'):
            loop = 1
        name = string.capwords(str(name))
        name = "'"+name+"'"
        sql_command = "SELECT * FROM {}.{} where bk_name = {};".format(str(schema), "book", str(name))
        data = load_db(sql_command)
        if(not data["bk_id"]):
            print("Sorry that book doesnt exist!")
            ans = input("Try another?(y or n) ")
            if(ans == 'n' or ans == 'N'):
                loop == 1
        else:
            d = []
            p = {"Name": None}, {"Price" : None}, {"Author" : None},{"ISBN-13": None},{"Genre":None},{"Pages":None},{"Type":None},{"Language":None},{"Publisher": None},{"Published" : None}
            for i in data["bk_name"]:
                pr = "$" + str(data["bk_price"][i])
                p = {"Name": data["bk_name"][i]}, {"Price" : pr}, {"Author" : data["bk_auth"][i]},{"ISBN-13": data["bk_isbn"][i]},{"Genre":data["bk_genre"][i]},{"Pages":data["bk_pages"][i]},{"Type":data["bk_type"][i]},{"Language":data["bk_lang"][i]},{"Publisher": data["bk_pub"][i]},{"Published" : data["bk_published"][i]}
                d.append(p)
            print()
            print("More info:")
            pprint.pprint(d)
            print()
            loop = 1

def search():
    loop = 0
    while(not loop):
        print()
        print("Enter 'e' to exit")
        print("You can enter a book name, author, isbn, price, etc.")
        print("To enter more than one attribute, separate them by a ',' ")
        print()
        se = input("Search: ")
        allq = []
        if(se):
            if(se == 'e'):
                loop = 1
            #loop through se to find and separate by commas
            elif(',' in se):
                #se is now a list
                se = se.split(',')
                for q in se:
                    q = string.capwords(q)
                    q = "'"+q+"'"
                    com = "select * from global_search({})".format(q)
                    res = load_db(com)
                    allq.append(res)
            else:
                se = string.capwords(se)
                se = "'"+se+"'"
                com = "select * from global_search({})".format(se)
                res = load_db(com)
                allq.append(res)

            emptys = 0
            for r in allq:
                #print(r)
                if(r['schemaname']):
                    if(r['schemaname'][0]):
                        #find the book and print it
                        allbooks = []
                        #if one query results in multiples
                        if(len(r['schemaname']) > 1):
                            #print(r['rowctid'][0])
                            for i in range(len(r['rowctid'])):
                                s = "'"+r['rowctid'][i]+"'"
                                #print(s)
                                exactq = "select * from {}.{} where ctid = {}; ".format(str(r['schemaname'][0]), str(r['tablename'][0]),str(s))
                                res = load_db(exactq)
                                p={}
                                for i in res["bk_name"]:
                                    pr = "$" + str(res["bk_price"][i])
                                    p.update({res["bk_name"][i] : pr})
                                pprint.pprint(p)
                        else:
                            s = "'"+r['rowctid'][0]+"'"
                            exactq = "select * from {}.{} where ctid = {};".format(str(r['schemaname'][0]), str(r['tablename'][0]),str(s))
                            res = load_db(exactq)
                            p={}
                            for i in res["bk_name"]:
                                pr = "$" + str(res["bk_price"][i])
                                p.update({res["bk_name"][i] : pr})
                            pprint.pprint(p)
                else:
                    emptys += 1
                    if(emptys == len(allq)):
                        ans = input("Didn't find anyting, wanna try again? ")
                        if(ans == 'n' or ans == 'N'):
                            loop = 1
            loop = 1
        else:
            print("Please enter anything or 'e' to exit")

"""
def load_data(schema, table):

    sql_command = "SELECT * FROM {}.{};".format(str(schema), str(table))
    print (sql_command)

    # Load the data
    data = pd.read_sql(sql_command, conn)

    print(data.shape)
    return (data)
"""
