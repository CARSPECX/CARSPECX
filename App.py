from flask import Flask, render_template, request, redirect
from db_config import get_db

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT id, brand, model, price, fuel_type, transmission, image
        FROM cars
    """)
    cars = cur.fetchall()
    cur.close()
    db.close()
    return render_template("index.html", cars=cars)

# ---------------- DETAILS ----------------
@app.route("/details/<int:id>")
def details(id):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM cars WHERE id=%s", (id,))
    car = cur.fetchone()
    cur.close()
    db.close()
    return render_template("details.html", car=car)

# ---------------- FINDER ----------------
@app.route("/finder", methods=["GET", "POST"])
def finder():
    db = get_db()
    cur = db.cursor(dictionary=True)
    query = "SELECT * FROM cars WHERE 1=1"
    values = []

    if request.method == "POST":
        if request.form.get("max_price"):
            query += " AND price <= %s"
            values.append(request.form["max_price"])

        if request.form.get("fuel"):
            query += " AND fuel_type = %s"
            values.append(request.form["fuel"])

        if request.form.get("transmission"):
            query += " AND transmission = %s"
            values.append(request.form["transmission"])

        if request.form.get("body_type"):
            query += " AND body_type = %s"
            values.append(request.form["body_type"])

        if request.form.get("sunroof"):
            query += " AND sunroof = %s"
            values.append(request.form["sunroof"])

        if request.form.get("seating"):
            query += " AND seating_capacity >= %s"
            values.append(request.form["seating"])

    cur.execute(query, tuple(values))
    cars = cur.fetchall()
    cur.close()
    db.close()
    return render_template("finder.html", cars=cars)

# ---------------- RECOMMEND ----------------
@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    cars = []
    if request.method == "POST":
        budget = int(request.form["budget"])
        fuel = request.form["fuel"]
        transmission = request.form["transmission"]
        seating = int(request.form["seating"])

        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM cars WHERE price <= %s", (budget,))
        data = cur.fetchall()

        for car in data:
            score = 0
            if car["fuel_type"] == fuel: score += 2
            if car["transmission"] == transmission: score += 2
            if car["seating_capacity"] >= seating: score += 2
            if car["sunroof"] == "Yes": score += 1
            if car["airbags"] >= 6: score += 1
            if car["safety_rating"] in ["4", "5"]: score += 1
            car["score"] = score
            cars.append(car)

        cars = sorted(cars, key=lambda x: x["score"], reverse=True)
        cur.close()
        db.close()

    return render_template("recommend.html", cars=cars)

# ---------------- EMI ----------------
@app.route("/emi", methods=["GET", "POST"])
def emi():
    emi_val = None
    if request.method == "POST":
        price = float(request.form["price"])
        rate = float(request.form["rate"]) / 1200
        months = int(request.form["months"])
        emi_val = (price * rate * (1+rate)**months) / ((1+rate)**months - 1)
    return render_template("emi.html", emi=emi_val)

# ---------------- COMPARE ----------------
@app.route("/compare", methods=["GET", "POST"])
def compare():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT id, brand, model FROM cars")
    allcars = cur.fetchall()

    if request.method == "POST":
        c1 = request.form["car1"]
        c2 = request.form["car2"]

        cur.execute("SELECT * FROM cars WHERE id=%s", (c1,))
        car1 = cur.fetchone()
        cur.execute("SELECT * FROM cars WHERE id=%s", (c2,))
        car2 = cur.fetchone()
        cur.close()
        db.close()
        return render_template("compare.html", car1=car1, car2=car2)

    cur.close()
    db.close()
    return render_template("compare_select.html", allcars=allcars)

# ---------------- ADMIN ----------------
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if request.method == "POST":
        user = request.form["username"]
        pwd = request.form["password"]

        db = get_db()
        cur = db.cursor(dictionary=True)
        cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (user, pwd))
        admin = cur.fetchone()
        cur.close()
        db.close()

        if admin:
            return redirect("/admin/dashboard")
        return "Invalid Login"

    return render_template("admin.html")

# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin/dashboard")
def dashboard():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT * FROM cars")
    cars = cur.fetchall()
    cur.close()
    db.close()
    return render_template("admin_dashboard.html", cars=cars)

# ---------------- DELETE ----------------
@app.route("/admin/delete/<int:id>")
def delete(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM cars WHERE id=%s", (id,))
    db.commit()
    cur.close()
    db.close()
    return redirect("/admin/dashboard")

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
