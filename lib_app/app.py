import func as func
import current_user as cu

def main():
    print("Welcome to Look Inna Book Bookstore!")
    signin = False
    while(signin == False):
        ops= ["Sign in", "Sign up", "Browse books", "Exit"]
        print("Please select an option from the list below by number")
        choice = func.pr_menu(ops)
        if(choice == 0):
            func.signin()
            signin=True
        elif(choice == 1):
            func.signup()
        elif(choice == 2):
            print(func.browse())
            func.browse_menu()
        elif(choice == 3):
            signin = True
            print("Come back soon!")
        else:
            print("Thats not an option")

main()
