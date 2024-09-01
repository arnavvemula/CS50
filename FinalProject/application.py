import os
import random
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from datetime import datetime
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, lookup, usd

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd
app.jinja_env.globals.update(usd=usd, lookup=lookup, int=int)

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["PREFERRED_URL_SCHEME"] = 'https'
app.config["DEBUG"] = False
Session(app)

db = SQL("sqlite:///remember.db")




@app.route('/')
@login_required
def index():
    user=db.execute("SELECT username FROM users WHERE id=:user_id", user_id=session["user_id"])
    username= user[0]["username"]
    return render_template("index.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Forget user_id
    session.clear()
    if request.method == "POST":
        password=request.form.get("password")
        confirmation=request.form.get("confirmation")
        username=request.form.get("username")
        try:
           new_user_id = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",username=request.form.get("username"),hash=generate_password_hash(request.form.get("password")))

        except:
            return apology("Username taken", 400)
        if not username:
            return apology("Must provide username",400)
        if not password:
            return apology("Must provide password",400)
        if not confirmation:
            return apology("Must provide password confirmation",400)
        if new_user_id is None:
            return apology("Restering error", 403)
        if password != confirmation:
            return apology("the confirmation and password must match",400)

        session["user_id"] = new_user_id
        return redirect("/")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    """Log user out"""

    session.clear()


    return redirect(url_for("login"))



@app.route("/encrypt", methods=["GET", "POST"])
@login_required
def encrypt():
    if request.method == "POST":
        depend="EN€RYP₮!ON"
        depend=depend
        dencrypt="encrypt"
        message = request.form.get("mess")
        alphabet = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+{}|:<>?=-[]\;',./`~ABCDEFGHIJKLMNOPQRSTUVWXYZ "
        key =request.form.get("key")
        if not key:
            return apology("Must provide key")
        if not request.form.get("key").isdigit():
            return apology("Must provide Numeric key")
        if not message:
            return apology("Must provide message")
        encrypt =''
        for i in message:
            position = alphabet.find(i)
            new_position = (position+ int(key) )%94
            encrypt += alphabet[new_position]
        output = (encrypt)
        return render_template("display.html",output=output, message=message,key= key, depend=depend, dencrypt=dencrypt )
    else:
        return render_template("eform.html")

@app.route("/decrypt", methods=["GET", "POST"])
@login_required
def decrypt():
    if request.method == "POST":
        depend="DE€RYP₮!ON"
        depend=depend
        dencrypt="decrypt"
        for i in range(1):
          keygen = (random.randint(11111111111, 999999999999999))
        print("")
        message = request.form.get('mess')
        alphabet = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+{}|:<>?=-[]\;',./`~ABCDEFGHIJKLMNOPQRSTUVWXYZ "
        key = request.form.get("key")
        if not key:
            return apology("Must provide key")
        if not request.form.get("key").isdigit():
            return apology("Must provide Numeric key")
        if not message:
            return apology("Must provide message")
        encrypt =''
        for i in message:
          position = alphabet.find(i)
          newposition = (position+ -int(key) )%94
          encrypt += alphabet [newposition]
        output = (encrypt)
        return render_template("display.html",output=output, message=message, key=key, depend=depend, dencrypt=dencrypt)
    else:
        return render_template("dform.html")



@app.route("/calculator", methods=["GET","POST"])
def calculator():
    if request.method=="GET":
        return render_template("calculator.html")
    
@app.route("/translator", methods=["GET","POST"])
def translator():
    if request.method=="GET":
        return render_template("translator.html")

@app.route("/basical", methods=["GET","POST"])
def basic():
    if request.method=="GET":
        return render_template("basical.html")

@app.route("/scientific", methods=["GET","POST"])
def sci():
    if request.method=="GET":
        return render_template("scientific.html")

@app.route("/change_pass", methods=["GET","POST"])
@login_required
def change_pass():
    if request.method=="POST":
        password=db.execute("SELECT hash FROM users WHERE id=:user_id", user_id=session["user_id"])
        new_password=request.form.get("new_password")
        old_password=request.form.get("old_password")
        confirmation=request.form.get("confirmation")
        if not new_password:
            return apology("Must provide new password",400)
        if not old_password:
            return apology("Must provide old password",400)
        if not confirmation:
            return apology("Must provide password confirmation",400)
        if len(password) != 1 or not check_password_hash(password[0]["hash"], request.form.get("old_password")):
            return apology("invalid password", 400)
        if new_password != confirmation:
            return apology("the confirmation and password must match",400)
        if new_password == old_password:
            return apology("the new password and old password match",400)

        db.execute("UPDATE users SET hash=:hash WHERE id=:user_id", hash=generate_password_hash(request.form.get("new_password")), user_id=session["user_id"])# asks for password,old password, and new password to see for error checking and if they all fit the criteria then it changes the password
        flash("Succesfully updated password")
        return redirect("/")
    else:
        return render_template("change_pass.html")

@app.route("/py", methods=["GET","POST"])
def py():
    if request.method=="GET":
        return render_template("py.html")

@app.route("/scratch", methods=["GET","POST"])
def scratch():
    if request.method=="GET":
        return render_template("scratch.html")

@app.route("/text", methods=["GET","POST"])
def text():
    if request.method == "POST":
        special_char="!@#$%^&*()-+?_=,<>/"
        numbers="1234567890"

        space = 0
        alphabets = 0
        special=0
        digits=0

        ask= request.form.get("text")

        for i in range(len(ask)):
            if(ask[i].isalpha()):
                alphabets = alphabets + 1
            elif (ask[i] in special_char):
                special = special + 1
            elif(ask[i] in numbers):
                digits = digits + 1
            elif ask[i] == " ":
                    space += 1
        if not ask:
            return apology("Must provide field")

        size=len(ask)

        return render_template("text_display.html", space=space, alphabets=alphabets, special=special, digits=digits, size=size, ask=ask)
    else:
        return render_template("text.html")

@app.route("/info", methods=["GET", "POST"])
def info():
    if request.method == "POST":
        Website=request.form.get("web")
        username=request.form.get("username")
        passkey=request.form.get("password")
        user_id=session["user_id"]


        e=enc(passkey)

        if not Website:
           return apology("Must provide Website",400)
        elif not username:
            return apology("Must provide username",400)
        elif not passkey:
            return apology("Must provide password",400)
        else:
            db.execute("INSERT INTO info (website, username, password, user_id) VALUES(?, ?, ?, ?)",Website,username, e, user_id)

        Info= db.execute("SELECT * FROM info WHERE user_id=:user_id", user_id=session["user_id"])
        Password=db.execute("SELECT password FROM info WHERE user_id=:user_id", user_id=session["user_id"])
        decryption=[]
        for password in Password:
            de=password['password']
            d=dec(de)
            decryption.append(d)
            print(decryption)
        return render_template("personal.html", Info=Info, decryption=decryption) #rempromts if mising

    else:
        Info= db.execute("SELECT * FROM info WHERE user_id=:user_id", user_id=session["user_id"])
        Password=db.execute("SELECT password FROM info WHERE user_id=:user_id", user_id=session["user_id"])
        decryption=[]
        for password in Password:
            de=password['password']
            d=dec(de)
            decryption.append(d)
            print(decryption)

        return render_template("personal.html", Info=Info,decryption=decryption)#continues normally

@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    if request.method == "POST":
        iden=id
        db.execute("DELETE FROM info WHERE id=?",iden)
    return redirect("/info")


def dec(password):
    for i in range(1):
      keygen = (random.randint(11111111111, 999999999999999))
    print("")
    message = password
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+{}|:<>?=-[]\;',./`~ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    key = 36
    encrypt =''
    for i in message:
      position = alphabet.find(i)
      newposition = (position+ -int(key) )%94
      encrypt += alphabet [newposition]
    return (encrypt)

def enc(password):
    message = password
    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()_+{}|:<>?=-[]\;',./`~ABCDEFGHIJKLMNOPQRSTUVWXYZ "
    key = 36
    encrypt =''
    for i in message:
        position = alphabet.find(i)
        new_position = (position+ int(key) )%94
        encrypt += alphabet[new_position]
    return (encrypt)


if __name__== '__main__':
    app.run()