from flask import Flask, render_template, request, redirect, session
from database import create_tables
from auth import register_user, login_user
from finance import add_transaction, get_transactions, get_summary

app = Flask(__name__)
app.secret_key = "secretkey"

create_tables()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = login_user(
            request.form["username"],
            request.form["password"]
        )
        if user:
            session["user_id"] = user[0]
            return redirect("/dashboard")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        success = register_user(
            request.form["username"],
            request.form["password"]
        )
        if success:
            return redirect("/")
    return render_template("register.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    if request.method == "POST":
        add_transaction(
            session["user_id"],
            request.form["type"],
            request.form["category"],
            float(request.form["amount"])
        )

    transactions = get_transactions(session["user_id"])
    income, expense, balance = get_summary(session["user_id"])

    return render_template(
        "dashboard.html",
        transactions=transactions,
        income=income,
        expense=expense,
        balance=balance
    )


@app.route("/report")
def report():
    if "user_id" not in session:
        return redirect("/")

    transactions = get_transactions(session["user_id"])
    income, expense, balance = get_summary(session["user_id"])

    return render_template(
        "report.html",
        transactions=transactions,
        income=income,
        expense=expense,
        balance=balance
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
