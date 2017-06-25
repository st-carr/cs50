from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from passlib.apps import custom_app_context as pwd_context
from tempfile import gettempdir

from helpers import *

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

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = gettempdir()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


def sell_stock(symbol, shares):
        # get current price
        dict = lookup(symbol)
        if dict == None:
            return apology("Sorry, this is not a valid symbol.")
        
        stock_symbol = dict["symbol"]
        stock_symbol = stock_symbol.upper()
        sell_symbol = symbol
        sell_symbol = sell_symbol.upper()
        

        # query database for username and stock holdings
        rows = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])
        portfolio_rows = db.execute("SELECT * FROM portfolio WHERE symbol = :symbol AND user_id = :id", symbol = sell_symbol, id = session["user_id"])

        # query database to check if portolio is empty
        insert_rows = db.execute("SELECT * FROM portfolio WHERE user_id = :id", id = session["user_id"])

        # bank roll
        bank = rows[0]["cash"]
        # current stock price
        sell_price = dict["price"]
        # amout to sell
        sell_qty = float(shares)
        # total value of holdings to sell
        sell_total = sell_price * sell_qty

        # check if the database is empty for this user
        if not portfolio_rows:
            return apology("You do not currently own this stock")

        # current holdings
        portfolio_qty = portfolio_rows[0]["qty"]
        
        # calculate new bank and share holdings
        bank = bank + sell_total
        portfolio_qty -= int(sell_qty)        
        # check if the user is trying to sell more than they own        
        if portfolio_qty < 0:
            return apology("Not have enough shares.")
        # delete this stock from the portfolio if they are selling all shares
        elif portfolio_qty == 0:
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = bank, id = session["user_id"])
            db.execute("DELETE FROM portfolio WHERE symbol = :symbol AND user_id = :id", symbol = sell_symbol, id = session["user_id"])
            db.execute("INSERT INTO history (user_id, symbol, qty, action, price) VALUES (:user_id, :symbol, :qty, :action, :price)", user_id = session["user_id"], symbol = sell_symbol, qty = sell_qty, action = "sell", price = sell_price)
        # otherwise, update this stock with the new share total
        else:
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = bank, id = session["user_id"])
            db.execute("UPDATE portfolio SET qty = :qty WHERE symbol = :symbol AND user_id = :id", qty = portfolio_qty, symbol = sell_symbol, id = session["user_id"])
            db.execute("INSERT INTO history (user_id, symbol, qty, action, price) VALUES (:user_id, :symbol, :qty, :action, :price)", user_id = session["user_id"], symbol = sell_symbol, qty = sell_qty, action = "sell", price = sell_price)
        # redirect user to home page
        return 0


def buy_stock(symbol, shares):
    # get current price
    dict = lookup(symbol)
    if dict == None:
        return apology("Sorry, this is not a valid symbol.")
    
    stock_symbol = dict["symbol"]
    stock_symbol = stock_symbol.upper()
    portfolio_symbol = symbol
    portfolio_symbol = portfolio_symbol.upper()
    

    # query database for username
    rows = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])
    portfolio_rows = db.execute("SELECT * FROM portfolio WHERE symbol = :symbol AND user_id = :id", symbol = portfolio_symbol, id = session["user_id"])
    insert_rows = db.execute("SELECT * FROM portfolio WHERE user_id = :id", id = session["user_id"])


    bank = rows[0]["cash"]
    buy_price = dict["price"]
    buy_qty = float(shares)
    buy_total = buy_price * buy_qty
    insert_symbol = symbol
    insert_symbol = insert_symbol.upper()

    if buy_total > bank:
        return apology("NOT ENOUGH CASH")
    elif not insert_rows:
        db.execute("INSERT INTO portfolio (user_id, symbol, qty) VALUES (:user_id, :symbol, :qty)", 
        user_id = session["user_id"], symbol = insert_symbol, qty = buy_qty)
        bank -= buy_total
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = bank, id = session["user_id"])
        db.execute("INSERT INTO history (user_id, symbol, qty, action) VALUES (:user_id, :symbol, :qty, :action)", user_id = session["user_id"], symbol = insert_symbol, qty = buy_qty, action = "buy")
    elif not portfolio_rows:
        db.execute("INSERT INTO portfolio (user_id, symbol, qty) VALUES (:user_id, :symbol, :qty)", user_id = session["user_id"], symbol = insert_symbol, qty = buy_qty)
        bank -= buy_total
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = bank, id = session["user_id"])
        db.execute("INSERT INTO history (user_id, symbol, qty, action, price) VALUES (:user_id, :symbol, :qty, :action, :price)", user_id = session["user_id"], symbol = insert_symbol, qty = buy_qty, action = "buy", price = buy_price)
    elif portfolio_rows[0]["symbol"] ==  portfolio_symbol:
        curr_shares = portfolio_rows[0]["qty"]
        new_shares = curr_shares + buy_qty
        bank -= buy_total
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = bank, id = session["user_id"])
        db.execute("UPDATE portfolio SET qty = :qty WHERE symbol = :symbol AND user_id = :id", qty = new_shares, symbol = portfolio_symbol, id = session["user_id"])
        db.execute("INSERT INTO history (user_id, symbol, qty, action, price) VALUES (:user_id, :symbol, :qty, :action, :price)", user_id = session["user_id"], symbol = insert_symbol, qty = buy_qty, action = "buy", price = buy_price)
    
    return 0



@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Get user portfolio."""
    if request.method == "POST":
        rows_db = db.execute("SELECT * FROM users INNER JOIN portfolio ON users.id = portfolio.user_id WHERE users.id = :id", id = session["user_id"])
        for j in range(len(rows_db)):
            try:
                text_index = "qty_" + str(j+1)
                symbol_index = "".join(("symbol_", str(j+1)))
                action_index = "action_" + str(j+1)
                num = int(request.form.get(text_index))
            except:
                continue
            else:
                if num > 0:
                    if request.form.get(action_index) == "buy":
                        buy_stock(rows_db[j]["symbol"], num)
                    elif request.form.get(action_index) == "sell":
                        sell_stock(rows_db[j]["symbol"], num)
        
        
        dict = []
        rows_db = db.execute("SELECT * FROM users INNER JOIN portfolio ON users.id = portfolio.user_id WHERE users.id = :id", id = session["user_id"])
        stock_total = 0
        len_rows = len(rows_db)
        for i in range(len_rows):
            dict.append(lookup(rows_db[i]["symbol"]))
            stock_total = stock_total + (float(rows_db[i]["qty"]) * dict[i]["price"])
        
        row_data = zip(rows_db, dict)
        if not rows_db:
            return render_template("index.html")
        else:
            return render_template("index.html", datas = row_data, cash = rows_db[0]["cash"], stock_total = stock_total)
    else:    
        dict = []
        rows_db = db.execute("SELECT * FROM users INNER JOIN portfolio ON users.id = portfolio.user_id WHERE users.id = :id", id = session["user_id"])
        stock_total = 0
        len_rows = len(rows_db)
        for i in range(len_rows):
            dict.append(lookup(rows_db[i]["symbol"]))
            stock_total = stock_total + (float(rows_db[i]["qty"]) * dict[i]["price"])
        
        row_data = zip(rows_db, dict)
        if not rows_db:
            return render_template("index.html")
        else:
            return render_template("index.html", datas = row_data, cash = rows_db[0]["cash"], stock_total = stock_total)





@app.route("/changepw", methods=["GET", "POST"])
@login_required
def changepw():
    """Change user password."""
    if request.method == "POST":
        
        # query database for user
        rows = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
    
        if  pwd_context.verify(request.form.get("curr_password"), rows[0]["hash"]) and request.form.get("new_password") == request.form.get("confirm_new_password"):
            hash = pwd_context.hash(request.form.get("new_password"))
            db.execute("UPDATE users SET hash = :hash WHERE id = :id", hash = hash, id = session["user_id"])
                    
            # redirect user to home page
            return redirect(url_for("index"))
    else:
        return render_template("changepw.html")




@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    if request.method == "POST":
        # check for proper form usage    
        if not request.form.get("symbol"):
            return apology("Must provide a symbol")
        elif not request.form.get("qty"):
            return apology("Must enter a quantity")

        # get current price
        dict = lookup(request.form.get("symbol"))
        if dict == None:
            return apology("Sorry, this is not a valid symbol.")
        
        stock_symbol = dict["symbol"]
        stock_symbol = stock_symbol.upper()
        portfolio_symbol = request.form.get("symbol")
        portfolio_symbol = portfolio_symbol.upper()
        

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])
        portfolio_rows = db.execute("SELECT * FROM portfolio WHERE symbol = :symbol AND user_id = :id", symbol = portfolio_symbol, id = session["user_id"])
        insert_rows = db.execute("SELECT * FROM portfolio WHERE user_id = :id", id = session["user_id"])


        bank = rows[0]["cash"]
        buy_price = dict["price"]
        buy_qty = float(request.form.get("qty"))
        buy_total = buy_price * buy_qty
        insert_symbol = request.form.get("symbol")
        insert_symbol = insert_symbol.upper()

        if buy_total > bank:
            return apology("NOT ENOUGH CASH")
        elif not insert_rows:
            db.execute("INSERT INTO portfolio (user_id, symbol, qty) VALUES (:user_id, :symbol, :qty)", 
            user_id = session["user_id"], symbol = insert_symbol, qty = buy_qty)
            bank -= buy_total
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = bank, id = session["user_id"])
            db.execute("INSERT INTO history (user_id, symbol, qty, action) VALUES (:user_id, :symbol, :qty, :action)", user_id = session["user_id"], symbol = insert_symbol, qty = buy_qty, action = "buy")
        elif not portfolio_rows:
            db.execute("INSERT INTO portfolio (user_id, symbol, qty) VALUES (:user_id, :symbol, :qty)", user_id = session["user_id"], symbol = insert_symbol, qty = buy_qty)
            bank -= buy_total
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = bank, id = session["user_id"])
            db.execute("INSERT INTO history (user_id, symbol, qty, action, price) VALUES (:user_id, :symbol, :qty, :action, :price)", user_id = session["user_id"], symbol = insert_symbol, qty = buy_qty, action = "buy", price = buy_price)
        elif portfolio_rows[0]["symbol"] ==  portfolio_symbol:
            curr_shares = portfolio_rows[0]["qty"]
            new_shares = curr_shares + buy_qty
            bank -= buy_total
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = bank, id = session["user_id"])
            db.execute("UPDATE portfolio SET qty = :qty WHERE symbol = :symbol AND user_id = :id", qty = new_shares, symbol = portfolio_symbol, id = session["user_id"])
            db.execute("INSERT INTO history (user_id, symbol, qty, action, price) VALUES (:user_id, :symbol, :qty, :action, :price)", user_id = session["user_id"], symbol = insert_symbol, qty = buy_qty, action = "buy", price = buy_price)
        # redirect user to home page
        return redirect(url_for("index"))
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    rows_db = db.execute("SELECT * FROM history WHERE user_id = :id", id = session["user_id"])

    if not rows_db:
        return render_template("history.html")
    else:
        return render_template("history.html", rows = rows_db)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get("password"), rows[0]["hash"]):
            return apology("invalid username and/or password")

        # remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        dict = lookup(request.form.get("symbol"))
        if dict == None:
            return apology("Sorry, this is not a valid symbol.")
        return render_template("quoted.html", tickers=dict)
    elif request.method == "GET":
        return render_template("quote.html")
        
        
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    session.clear()
    if request.method == "POST":
        
        # query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username", username=request.form.get("username"))

        if not request.form.get("username"):
            return apology("Must provide a username")
        elif len(rows) == 1:
            return apology("This Username already exists")
        elif len(rows) == 0:
            if request.form.get("password") == request.form.get("confirm_password"):
                hash = pwd_context.hash(request.form.get("password"))
                db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username = request.form.get("username"), hash = hash)
                
        # remember which user has logged in
        session["user_id"] = rows[0]["id"]
            
        # redirect user to home page
        return redirect(url_for("index"))
    
    else:
        return render_template("register.html")



@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    if request.method == "POST":
        # check for proper form usage    
        if not request.form.get("symbol"):
            return apology("Must provide a symbol")
        elif not request.form.get("qty"):
            return apology("Must enter a quantity")

        # get current price
        dict = lookup(request.form.get("symbol"))
        if dict == None:
            return apology("Sorry, this is not a valid symbol.")
        
        stock_symbol = dict["symbol"]
        stock_symbol = stock_symbol.upper()
        sell_symbol = request.form.get("symbol")
        sell_symbol = sell_symbol.upper()
        

        # query database for username and stock holdings
        rows = db.execute("SELECT * FROM users WHERE id = :id", id = session["user_id"])
        portfolio_rows = db.execute("SELECT * FROM portfolio WHERE symbol = :symbol AND user_id = :id", symbol = sell_symbol, id = session["user_id"])

        # query database to check if portolio is empty
        insert_rows = db.execute("SELECT * FROM portfolio WHERE user_id = :id", id = session["user_id"])

        # bank roll
        bank = rows[0]["cash"]
        # current stock price
        sell_price = dict["price"]
        # amout to sell
        sell_qty = float(request.form.get("qty"))
        # total value of holdings to sell
        sell_total = sell_price * sell_qty

        # check if the database is empty for this user
        if not portfolio_rows:
            return apology("You do not currently own this stock")

        # current holdings
        portfolio_qty = portfolio_rows[0]["qty"]
        
        # calculate new bank and share holdings
        bank = bank + sell_total
        portfolio_qty -= int(sell_qty)        
        # check if the user is trying to sell more than they own        
        if portfolio_qty < 0:
            return apology("Not have enough shares.")
        # delete this stock from the portfolio if they are selling all shares
        elif portfolio_qty == 0:
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = bank, id = session["user_id"])
            db.execute("DELETE FROM portfolio WHERE symbol = :symbol AND user_id = :id", symbol = sell_symbol, id = session["user_id"])
            db.execute("INSERT INTO history (user_id, symbol, qty, action, price) VALUES (:user_id, :symbol, :qty, :action, :price)", user_id = session["user_id"], symbol = sell_symbol, qty = sell_qty, action = "sell", price = sell_price)
        # otherwise, update this stock with the new share total
        else:
            db.execute("UPDATE users SET cash = :cash WHERE id = :id", cash = bank, id = session["user_id"])
            db.execute("UPDATE portfolio SET qty = :qty WHERE symbol = :symbol AND user_id = :id", qty = portfolio_qty, symbol = sell_symbol, id = session["user_id"])
            db.execute("INSERT INTO history (user_id, symbol, qty, action, price) VALUES (:user_id, :symbol, :qty, :action, :price)", user_id = session["user_id"], symbol = sell_symbol, qty = sell_qty, action = "sell", price = sell_price)
        # redirect user to home page
        return redirect(url_for("index"))
    else:
        return render_template("sell.html")


