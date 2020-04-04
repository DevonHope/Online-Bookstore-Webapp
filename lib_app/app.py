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
