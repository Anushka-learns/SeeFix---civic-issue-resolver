import sqlite3
import uuid
from flask import Flask, render_template, request,redirect,session
import os
from predict import predict_image
from database import save_report
from database import init_db

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["image"]
    address = request.form["address"]

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    prediction = predict_image(filepath)

    save_report(filepath, prediction, address)
    complaint_id = "CIV-" + str(uuid.uuid4())[:8]

    return render_template("result.html", prediction=prediction, image=filepath)

@app.route("/dashboard")
def dashboard():
    from database import get_reports
    reports = get_reports()
    return render_template("dashboard.html", reports=reports)

@app.route("/resolve/<int:id>")
def resolve(id):
    if session.get("role") != "admin":
        return "Access Denied"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE reports SET status='Resolved' WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect("/dashboard")
@app.route("/login", methods=["POST"])
def login():
    role = request.form["role"]
    session["role"] = role

    if role == "admin":
        return redirect("/admin-dashboard")
    else:
        return redirect("/user-dashboard")


@app.route("/login", methods=["POST"])
def login_user():
    role = request.form["role"]

    if role == "admin":
        return redirect("/dashboard")
    else:
        return redirect("/")
    
@app.route("/user-dashboard")
def user_dashboard():
    return render_template("upload.html")

@app.route("/admin-dashboard")
def admin_dashboard():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reports")
    reports = cursor.fetchall()
    conn.close()

    return render_template("dashboard.html", reports=reports)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)