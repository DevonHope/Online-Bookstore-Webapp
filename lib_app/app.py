import func as func
import current_user as cu

#ACTS AS MENU
def signin():
    loop = 0
    while(loop == 0):
        uname = input("Username: ")
        pswd = input("Password: ")
        res = func.load_user(uname, pswd)
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

#ACTS AS MENU
def browse_menu():
    e = 0
    while(e == 0):
        ops = ["Sign in to buy book", "More info on specific book", "Main menu"]
        choice = func.pr_menu(ops)
        if(choice == 0):
            signin()
        elif(choice == 1):
            print(func.mor_book())
        elif(choice == 2):
            e = 1
        else:
            print("Thats not an option")

#ACTS AS MENU
def sin_menu():
    #New signed in user menu
    exit = 0
    while(exit == 0):
        ops=["Browse","Search","Cart","Sign out", "Exit"]
        print("Please select an option from the list below by number")
        choice = func.pr_menu(ops)
        if(choice == 0):
            print(func.browse())
        elif(choice == 1):
            func.search()
        elif(choice == 2):
            func.cart()
        elif(choice == 3):
            exit = 1
            print("Signed out!")
        elif(choice == 4):
            exit = 1
            print("Come back soon!")
        else:
            print("Thats not an option")

def main():
    print("Welcome to Look Inna Book Bookstore!")
    signin = False
    while(signin == False):
        ops= ["Sign in", "Sign up", "Browse books", "Exit"]
        print("Please select an option from the list below by number")
        choice = func.pr_menu(ops)
        if(choice == 0):
            signin()
            signin=True
        elif(choice == 1):
            func.signup()
        elif(choice == 2):
            print(func.browse())
            browse_menu()
        elif(choice == 3):
            signin = True
            print("Come back soon!")
        else:
            print("Thats not an option")

main()
