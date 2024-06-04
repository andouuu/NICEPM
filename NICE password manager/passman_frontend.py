from flask import Flask, render_template, request, make_response, redirect, session, jsonify, url_for

from config import CONFIG
from passman_api_shim import *
from passlib.hash import pbkdf2_sha256

app = Flask(__name__)
app.secret_key="andrians_secret"

@app.route("/", methods=["GET"])
def homepage():
    session_token = session.get('session_token')
    if session_token:
        accounts = list_of_accounts(session_token)
        return render_template("accounts/main.html", accounts=accounts, current_user=session['current_user'])
    else:
        return redirect(url_for('login'))  

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        session_token = user_login(username, password)
        if session_token:
            current_user= get_current_user(session_token)
            session['current_user']=current_user
            session['session_token'] = session_token  
            return redirect(url_for('homepage'))
        else:
            return render_template("accounts/login.html", error="Invalid username or password")
    else:
        return render_template("accounts/login.html")

@app.route("/logout",methods=["GET", "POST"])
def logout():
    current_user=session["current_user"]
    user_logout = logout_user(current_user["user_id"])
    if user_logout==200:
        session.pop('session_token', None)
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        success = user_register(username, password, email)
        if success[0]:
            return redirect("/login")
        else:
            return render_template("accounts/register.html", error="Registration failed. Please try again.")
    else:
        return render_template("accounts/register.html")

@app.route("/add", methods=["GET", "POST"])
def addaccount():
    if 'session_token' not in session:
        return redirect("/login")

    if request.method == "POST":
        account_name = request.form.get("account_name")
        account_password = request.form.get("account_password")
        account_website = request.form.get("account_website")
        account_user_id = session["current_user"]["user_id"]
        status_code = add_account(session['session_token'], account_name, account_password, account_website, account_user_id)
        if status_code == 201:
            return redirect("/")
        else:
            return render_template("accounts/new_account.html", error="Failed to add account. Please try again.")
    else:
        return render_template("accounts/new_account.html")

@app.route("/delete/<int:account_id>")
def deleteaccount(account_id):
    if 'session_token' not in session:
        return redirect("/login")

    delete_account(session['session_token'], account_id)
    return redirect("/")

@app.route("/edit/<int:account_id>", methods=["GET", "POST"])
def edit_account(account_id):
    if 'session_token' not in session:
        return redirect("/login")

    if request.method == "GET":
        account = get_account(session['session_token'], account_id)
        return render_template("accounts/edit_account.html", account=account)
    elif request.method == "POST":
        account = {
            "id": account_id,
            "username": request.form["account_name"],
            "password":  request.form["account_password"],
            "website":      request.form["account_website"]
        }
        id = update_account(session['session_token'], account)
        return redirect("/")
    
    return make_response("Invalid request", 400)

if __name__ == "__main__":
    app.run(host=CONFIG["frontend"]["listen_ip"], port=CONFIG["frontend"]["port"], debug=CONFIG["frontend"]["debug"])