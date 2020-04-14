import func as func
import current_user as cu
import admin as rp

def signin(user):
    loop = 0
    while(loop == 0):
        uname = input("Username: ")
        pswd = input("Password: ")
        if(uname == owner['user_username'][0] and pswd == owner['user_pswd'][0]):
            id = func.getInt("Owner ID: ")
            if(id == owner['user_id'][0]):
                owner_menu(user)
                loop=1
        else:
            res = func.load_user(uname, pswd)
            #print(res['user_pswd'])
            #print(res['user_id'])
            if(res['user_id'] or res is None):
                #print(res['user_pswd'][0])
                if(res['user_pswd'][0] == pswd and res['user_username'][0] == uname):
                    user.newUser(res['user_id'][0], res['user_name'][0], res['user_username'][0],\
                    res['user_biladdr'][0],res['user_shipaddr'][0],{'id':res['user_id'][0], 'books':{}})
                    print("You're signed in!")
                    print()
                    print("Signed in as: " + user.name)
                    print()
                    return 1
                    loop=1
            else:
                ans = input("Thats not right, try again?(y or n) ")
                if(ans == 'n' or ans == 'N'):
                    loop = 1
                    return 0

#ACTS AS MENU
def browse_menu(user):
    e = 0
    while(e == 0):
        opso = ["Sign in to buy book", "More info on specific book", "Main menu"] #signed out
        opsi = ["Add to cart", "More info on specific book", "Main menu"] #signed in
        if(user.getID() is None):
            choice = func.pr_menu(opso)
            if(choice == 0):
                signin(user)
            if(choice == 1):
                func.mor_book()
            elif(choice == 2):
                e = 1
            else:
                print("Thats not an option")
                print()
        else:
            choice = func.pr_menu(opsi)
            if(choice == 0):
                user = func.addCart(user)
            if(choice == 1):
                func.mor_book()
            elif(choice == 2):
                e = 1
            else:
                print("Thats not an option")
                print()

def check_menu(user):
    func.update_cart(user)
    #print cart
    func.cart(user)
    total = 0
    l = user.getCheck().values()
    for val in l:
        total += int(val)
    print("Total: $" + str(total))
    print()
    e = 0
    while(not e):
        #print cart, prices and total
        ops = ["Checkout", "Cancel"]
        choice = func.pr_menu(ops)
        if(choice == 0):
            loop=1
            while loop:
                tot = func.getInt("Type in the amount to pay: ")
                if(tot == total):
                    #generate a tracking number
                    # save to db
                    print("Checked out!")
                    print()
                    loop=0
                    e=1
                else:
                    ans = input("That wasn't the total, try again?(y or n) ")
                    if(ans == 'n' or ans == 'N'):
                        loop=0
            #here it should print a tracking number
            func.createTrack(user)
        elif(choice == 1):
            e = 1
            print("Cart saved!")
            print()

def owner_menu(user):
    print("ADMIN MENU")
    print()
    print("THIS DOESNT WORK YET")
    print()
    l = 1
    while l:
        ops=["Book management", "Pubisher management", "Reports management", "Sign out"]
        choice = func.pr_menu(ops)
        if(choice == 0):
            book_menu(user)
        elif(choice == 1):
            pubs_menu(user)
        elif(choice == 2):
            rep_menu(user)
        elif(choice == 3):
            print("byebye")
            print("SIGNED OUT OF ADMIN")
            print()
            l=0
        else:
            print("That isnt an option, try again")
            print()

def book_menu(user):
    print()
    print("Books Menu")
    print()
    l=1
    while l:
        ops=["Add Book", "Remove Book","Update Book", "Go back"]
        choice = func.pr_menu(ops)
        if(choice == 0):
            rp.addBook()
        elif choice == 1:
            rp.remBook()
        elif choice == 2:
            rp.upBook()
        elif choice == 3:
            l=0
            print()
        else:
            print("That isnt an option, try again")
            print()

def pubs_menu(user):
    print()
    print("Publisher Menu")
    print()
    l=1
    while l:
        ops=["Add Publisher", "Remove Publisher", "Update Publisher", "Go back"]
        choice = func.pr_menu(ops)
        if(choice == 0):
            rp.addPub()
        elif choice == 1:
            rp.remPub()
        elif choice == 2:
            rp.upPub()
        elif choice == 3:
            l=0
            print()
        else:
            print("That isnt an option, try again")
            print()

def rep_menu(user):
    print()
    print("Reports Menu")
    print()
    print("Sales per ")
    l=1
    while l:
        ops=["Expenses", "Genre", "Author", "Price", "Publisher", "Lanuage", "Type","Number of pages", "Go back"]
        choice = func.pr_menu(ops)
        if(choice == 0):
            rp.exp()
        elif choice == 1:
            rp.gen()
        elif choice == 2:
            rp.auth()
        elif choice == 3:
            rp.price()
        elif choice == 4:
            rp.publisher()
        elif choice == 5:
            rp.lang()
        elif choice == 6:
            rp.type()
        elif choice == 7:
            rp.numpages()
        elif choice == 8:
            l=0
            print()
        else:
            print("That isnt an option, try again")
            print()

#ACTS AS MENU
def sin_menu(user):
    #New signed in user menu
    exit = 0
    while(exit == 0):
        ops=["Browse","Search","Cart","Checkout", "Track Order","Sign out", "Exit"]
        print("Please select an option from the list below by number")
        choice = func.pr_menu(ops)
        if(choice == 0):
            func.browse()
            browse_menu(user)
        elif(choice == 1):
            func.search()
        elif(choice == 2):
            #displays users cart
            func.cart(user)
        elif(choice == 3):
            check_menu(user)
        elif choice == 4:
            func.getTrack(user)
        elif(choice == 5):
            exit = 1
            print("Signed out!")
            main()
        elif(choice == 6):
            exit = 1
            print("Come back soon!")
        else:
            print("Thats not an option")

def main():
    print("Welcome to Look Inna Book Bookstore!")
    sign = False
    while(not sign):
        ops= ["Sign in", "Sign up", "Search", "Browse books", "Exit"]
        print("Please select an option from the list below by number")
        choice = func.pr_menu(ops)
        if(choice == 0):
            if(signin(user)):
                sin_menu(user)
                sign=True
        elif(choice == 1):
            func.signup()
        elif(choice == 2):
            func.search()
        elif(choice == 3):
            func.browse()
            browse_menu(user)
            if(user.getID()):
                sin_menu(user)
        elif(choice == 4):
            sign = True
            print("Come back soon!")
        else:
            print("Thats not an option")

owner = func.getOwner()
user = cu.cuser(None, None, None, None, None, None)
main()
