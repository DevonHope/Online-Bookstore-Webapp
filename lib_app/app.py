import func as func

"""
def load_data(schema, table):

    sql_command = "SELECT * FROM {}.{};".format(str(schema), str(table))
    print (sql_command)

    # Load the data
    data = pd.read_sql(sql_command, conn)

    print(data.shape)
    return (data)
"""
def main():
    print("Welcome to Look Inna Book Bookstore!")
    signin = False
    while(signin == False):
        ops= ["Sign in", "Sign up", "Browse books", "getrownum", "Exit"]
        print("Please select an option from the list below by number")
        choice = func.pr_menu(ops)
        if(choice == 0):
            res = func.signin()
            if(res == 1):
                signin=True
                func.sin_menu()
        elif(choice == 1):
            func.signup()
        elif(choice == 2):
            print(func.browse())
            e = 0
            while(e == 0):
                ops = ["Sign in to buy book", "More info on specific book", "Main menu"]
                choice = func.pr_menu(ops)
                if(choice == 0):
                    res = func.signin()
                    if(res == 1):
                        signin=True
                        func.sin_menu()
                elif(choice == 1):
                    print(func.mor_book())
                elif(choice == 2):
                    e = 1
                elif(choice > len(ops) - 1):
                    print("Thats not an option")
        elif(choice == 3):
            signin = True
            print("Come back soon!")
        elif(choice > len(ops) - 1):
            print("Thats not an option")

main()
"""
# app.py for webapp in python
from flask import Flask, render_template
app = Flask(__name__)
@app.route('/')
def main():
    return render_template('html/index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('html/signup.html')

@app.route('/showSearch')
def showSearch():
    return render_template('html/search.html')

if __name__ == "__main__":
    app.run()
"""
