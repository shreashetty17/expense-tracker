from flask import Flask, render_template, request, redirect
import csv
import datetime
import os

app = Flask(__name__)


def get_expenses():
    expenses = []

    try:
        with open("expenses.csv", "r") as f:
            reader = csv.reader(f)
            expenses = list(reader)

    except FileNotFoundError:
        pass

    return expenses


def get_budget():
    try:
        with open("budget.txt", "r") as f:
            return float(f.read())

    except:
        return 0


@app.route("/")
def home():

    expenses = get_expenses()

    total = sum(
        float(row[3])
        for row in expenses
        if row
    )

    budget = get_budget()

    remaining = budget - total

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        budget=budget,
        remaining=remaining
    )


@app.route("/set_budget", methods=["POST"])
def set_budget():

    budget = request.form["budget"]

    with open("budget.txt", "w") as f:
        f.write(budget)

    return redirect("/")


@app.route("/add", methods=["POST"])
def add():

    name = request.form["name"]
    amount = request.form["amount"]
    category = request.form["category"]

    date = datetime.date.today()

    with open("expenses.csv", "a", newline="") as f:
        writer = csv.writer(f)

        writer.writerow([
            date,
            name,
            category,
            amount
        ])

    return redirect("/")


@app.route("/delete/<int:index>")
def delete(index):

    expenses = get_expenses()

    if 0 <= index < len(expenses):
        expenses.pop(index)

    with open("expenses.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(expenses)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)