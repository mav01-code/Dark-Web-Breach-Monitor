from flask import Flask, render_template, request, redirect, session, url_for
import requests
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = "password"

def get_connection():
    return mysql.connector.connect(host = "localhost", user = "root", password = "", database = "MONITOR")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form.get("email") or request.args.get("email")
        password = request.form.get("password") or request.args.get("password")
        if not email or not password:
            return "Email and password required", 400
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO REGISTER (EMAIL, PASSWORD) VALUES (%s, %s)", (email, password))
        conn.commit()
        conn.close()
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    email = request.form.get("email") or request.args.get("email")
    password = request.form.get("password") or request.args.get("password")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT email, password FROM REGISTER where email = '{email}' AND password = '{password}'")
    user = cursor.fetchone()
    conn.close()
    if user:
        session["user"] = email
        return redirect(url_for("dashboard"))
    else:
        return render_template("login.html", error="Invalid email or password")

@app.route("/dashboard", methods = ["GET"])
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("dashboard.html")

@app.route("/credential-storage", methods = ["GET"])
def credential_storage():
    if "user" not in session:
        return redirect(url_for("login"))
    return render_template("credential-storage.html")

@app.route("/credentials", methods = ["POST"])
def credentials():
    email = request.form.get("email") or request.args.get("email")
    password = request.form.get("password") or request.args.get("password")
    if not email or not password:
        return "Email and password required", 400
    conn = get_connection()
    cursor = conn.cursor()
    hashed = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    cursor.execute("SELECT 1 FROM CREDENTIALS WHERE EMAIL = %s", (email,))
    exists = cursor.fetchone()
    if not exists:
        cursor.execute("INSERT INTO CREDENTIALS (EMAIL, PASSWORD) VALUES (%s, %s)", (email, hashed))
        conn.commit()
    conn.close()
    return [email, hashed]

@app.route("/check", methods=["GET", "POST"])
def check():
    if "user" not in session:
        return redirect(url_for("login"))
    password = request.form.get("password") or request.args.get("password")
    if not password:
        return "Password required", 400

    password_hash = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    five = password_hash[:5]
    later = password_hash[5:]

    headers = {"User-Agent": "FlaskPasswordMonitorApp"}
    res = requests.get(f"https://api.pwnedpasswords.com/range/{five}", headers=headers)

    for line in res.text.splitlines():
        suffix, count = line.split(":")
        if suffix.upper() == later:
            return "FOUND IN DATA BREACH"

    return "SAFE"

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug = True)