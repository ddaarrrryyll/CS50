import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    users = db.execute("SELECT cash FROM users WHERE id = :user_id",
                        user_id=session["user_id"])

    stocks = db.execute("SELECT symbol, SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id AND symbol != :symbol GROUP BY symbol",
                        user_id=session["user_id"],
                        symbol='0')
    quotes = {}

    for stock in stocks:
        quotes[stock["symbol"]] = lookup(stock["symbol"])
        total_value = quotes[stock["symbol"]]["price"] * stock["total_shares"]
        db.execute("UPDATE transactions SET total_value = :total_value WHERE symbol = :symbol",
                    symbol=stock["symbol"],
                    total_value=total_value)

    cash_left = users[0]["cash"]

    cash_from_stocks = db.execute("SELECT SUM(DISTINCT total_value) as moolah FROM transactions WHERE user_id = :user_id",
                                    user_id=session["user_id"])

    total = cash_left + cash_from_stocks[0]["moolah"]

    return render_template("index.html", quotes=quotes, stocks=stocks, total=total, cash_left=cash_left)



@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    if request.method == "POST":

        stock = lookup(request.form.get("symbol"))
        # Ensure symbol was provided
        if not request.form.get("symbol"):
            return apology("indicate stock you want to buy", 400)

        elif stock == False:
            return apology("stock cannot be found", 400)

        # Ensure shares provided is a positive integer
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("provide a positive integer", 400)

        if shares <= 0:
            return apology("provide a positive integer", 400)


        # Obtain price of stock
        price = stock["price"]

        # Query database for user's current cash
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id",
                            user_id=session["user_id"])

        cash_left = rows[0]["cash"]

        # Total price
        total_price = shares * price
        if total_price > float(cash_left):
            return apology("You do not have enough funds", 400)


        # UPDATE finance.db
        db.execute("UPDATE users SET cash = cash - :price WHERE id = :user_id",
                    price=total_price,
                    user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, action) VALUES(:user_id, :symbol, :shares, :price, :action)",
                    user_id=session["user_id"],
                    symbol=request.form.get("symbol").upper(),
                    shares=shares,
                    price=price,
                    action="buy")

        flash("Bought!")
        return redirect("/")

    else:
        return render_template("buy.html")




@app.route("/check", methods=["GET"])
def check():
    """Return true if username available and 1 character or more, else false, in JSON format"""

    username = request.args.get("username")
    registered_users = db.execute("SELECT username FROM users WHERE username = :username",
                                    username=username)
    available_usernames = len(registered_users) == 0
    if len(request.args.get("username")) > 0 and available_usernames:
        return jsonify(True)
    else:
        return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    transactions = db.execute("SELECT symbol, shares, price, action, transacted FROM transactions WHERE user_id = :user_id AND symbol != '0' ORDER BY transacted ASC",
                                user_id=session["user_id"])
    return render_template("history.html", transactions=transactions)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    if request.method == "POST":
        if not request.form.get("symbol"):
            return apology("Must provide symbol", 400)

        stock = lookup(str(request.form.get("symbol")))
        if stock == False:
            return apology("Stock could not be found", 400)
        else:
            return render_template("quoted.html", stock = stock)

    else:
        return render_template("quote.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # clear session
    session.clear()

    if request.method == "POST":

        # ensure username provided
        if not request.form.get("username"):
            return apology("Must provide username", 400)

        # ensure password provided
        elif not request.form.get("password"):
            return apology("Must provide password", 400)

        # ensure password confirmation
        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("Passwords do not match", 400)


        password = str(request.form.get("password"))

        registered_users = db.execute("SELECT username FROM users")
        for registered_user in registered_users:
            if request.form.get("username") == registered_user["username"]:
                return apology("username has been taken")

        # add user into database
        result = db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)",
                            username=request.form.get("username"),
                            hash=generate_password_hash(password, method='pbkdf2:sha256', salt_length=8))

        rows = db.execute("SELECT * FROM users WHERE username = :username",
                            username=request.form.get("username"))

        session["user_id"] = rows[0]["id"]

        fml = db.execute("INSERT INTO transactions (user_id, symbol, shares, price, total_value, action) VALUES (:user_id, :symbol, :shares, :price, :total_value, :action)",
                            user_id=session["user_id"],
                            symbol='0',
                            shares='0',
                            price='0',
                            total_value='0',
                            action='0')

        # redirect user to index home page
        return redirect("/")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        quote = lookup(request.form.get("symbol"))

        if quote == False:
            return apology("indicate stock you want to buy", 400)

        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("provide positive integer", 400)
        if shares <= 0:
            return apology("provide positive integer", 400)

        # Obtain price of stock
        price = quote["price"]

        # Query database for user's stock holdings
        stocks = db.execute("SELECT SUM(shares) as total_shares FROM transactions WHERE user_id = :user_id AND symbol = :symbol AND action = :action GROUP BY symbol",
                            user_id=session["user_id"],
                            symbol=request.form.get("symbol"),
                            action="buy")

        if len(stocks) != 1 or stocks[0]["total_shares"] <= 0 or stocks[0]["total_shares"] < shares:
            return apology("you have insufficient" + str(request.form.get("symbol")) + "stocks", 400)

        # Query database for user's cash
        rows = db.execute("SELECT cash FROM users WHERE id = :user_id",
                            user_id = session["user_id"])
        cash_left = rows[0]["cash"]

        # Money from shares
        money_from_shares = price * shares

        # Money after
        moneyy = float(money_from_shares) + float(cash_left)


        # UPDATE finance.db
        db.execute("UPDATE users SET cash = :money WHERE id = :user_id",
                    money=moneyy,
                    user_id=session["user_id"])
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, action) VALUES(:user_id, :symbol, :shares, :price, :action)",
                    user_id=session["user_id"],
                    symbol=request.form.get("symbol").upper(),
                    shares= -shares,
                    price=price,
                    action="sell")

        flash("Sold!")
        return redirect("/")

    else:
        stocks = db.execute("SELECT symbol, SUM(DISTINCT shares) as total_shares FROM transactions WHERE user_id = :user_id AND action = :action GROUP BY symbol HAVING total_shares > 0",
                            user_id=session["user_id"],
                            action = "buy")
        return render_template("sell.html", stocks=stocks)


@app.route("/addfunds", methods=["GET", "POST"])
@login_required
def add_funds():
    """Add funds to user's cash"""
    if request.method == "POST":

        try:
            amount = float(request.form.get("amount"))

        except:
            return apology("ensure amount provided is a positive real number")

        db.execute("UPDATE users SET cash = cash + :amount WHERE id = :user_id",
                    user_id=session["user_id"],
                    amount=amount)
        flash("Funds added!")
        return redirect("/")

    else:
        return render_template("addfunds.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
