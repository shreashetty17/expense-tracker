from flask import Flask, render_template, request

app = Flask(__name__)

expenses = []
budget = 0


@app.route("/")
def home():

    total = 0
    for expense in expenses:
        total += float(expense["amount"])

    remaining = float(budget) - total if budget else 0

    return render_template(
        "index.html",
        expenses=expenses,
        total=total,
        budget=budget,
        remaining=remaining
    )


@app.route("/set_budget", methods=["POST"])
def set_budget():

    global budget
    budget = request.form["budget"]

    return home()


@app.route("/add", methods=["POST"])
def add():

    name = request.form["name"]
    amount = request.form["amount"]

    expenses.append({
        "name": name,
        "amount": amount
    })

    return home()


if __name__ == "__main__":
    app.run(debug=True)