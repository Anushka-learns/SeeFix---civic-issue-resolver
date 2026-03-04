from flask import Flask, render_template, request, redirect, session
import os
import sqlite3
from predict import predict_image
from database import save_report, get_reports, init_db
from flask import send_from_directory

app = Flask(__name__)
app.secret_key = "seefix_secret"

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- ROLE SELECTION ----------------
@app.route("/")
def role_page():
    return render_template("role.html")


@app.route("/select-role", methods=["POST"])
def select_role():
    session["selected_role"] = request.form["role"]
    return redirect("/login")


# ---------------- LOGIN ----------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    username = request.form["username"]
    password = request.form["password"]

    selected_role = session.get("selected_role")

    if not selected_role:
        return redirect("/")

    conn = sqlite3.connect("seefix.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role FROM users WHERE username=? AND password=?",
        (username, password),
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        actual_role = user[0]

        if actual_role != selected_role:
            return "Wrong role selected."

        session["username"] = username
        session["role"] = actual_role

        if actual_role == "admin":
            return redirect("/admin_dashboard")
        else:
            return redirect("/user_dashboard")

    return "Invalid login"


# ---------------- USER DASHBOARD ----------------
@app.route("/user_dashboard")
def user_dashboard():
    if session.get("role") != "user":
        return redirect("/")
    return render_template("user_dashboard.html")


# Upload page
@app.route("/upload_page")
def upload_page():
    if session.get("role") != "user":
        return redirect("/")
    return render_template("upload.html")


# ---------------- ADMIN DASHBOARD ----------------
@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("role") != "admin":
        return redirect("/")

    reports = get_reports()
    return render_template("admin_dashboard.html", reports=reports)


# ---------------- UPLOAD COMPLAINT ----------------
@app.route("/upload", methods=["POST"])
def upload():
    if "image" not in request.files:
        return "No file uploaded"

    file = request.files["image"]

    if file.filename == "":
        return "No selected file"

    # Save image
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(file_path)

    # Run AI prediction
    prediction, urgency, severity_score = predict_image(file_path)

    # Save to database
    complaint_id = save_report(
        prediction,
        urgency,
        severity_score,
        file_path
    )

    return render_template(
        "result.html",
        prediction=prediction,
        urgency=urgency,
        severity_score=severity_score,
        complaint_id=complaint_id,
        image="/" + file_path
    )

# ---------------- RESOLVE COMPLAINT ----------------
@app.route("/resolve/<int:report_id>")
def resolve(report_id):
    if session.get("role") != "admin":
        return redirect("/")

    conn = sqlite3.connect("seefix.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE reports SET status='Resolved' WHERE id=?", (report_id,))
    conn.commit()
    conn.close()

    return redirect("/admin_dashboard")


# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    init_db()
    app.run(debug=True)