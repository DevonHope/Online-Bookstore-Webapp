import func as func
import current_user as cu

def signin(user):
    loop = 0
    while(loop == 0):
        uname = input("Username: ")
        pswd = input("Password: ")
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
    e = 0
    while(not e):
        ops = [""]
        #print cart, prices and total

#ACTS AS MENU
def sin_menu(user):
    #New signed in user menu
    exit = 0
    while(exit == 0):
        ops=["Browse","Search","Cart","Checkout","Sign out", "Exit"]
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
            func.update_cart(user)
            check_menu(user)
        elif(choice == 4):
            exit = 1
            print("Signed out!")
            main()
        elif(choice == 5):
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

user = cu.cuser(None, None, None, None, None, None)
main()
