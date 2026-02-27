from flask import Flask, render_template, request, redirect, session, url_for
import requests
import mysql.connector
import hashlib

app = Flask(__name__)
app.secret_key = "password"

def get_connection():
    return mysql.connector.connect(host = "localhost", user = "root", password = "", database = "MONITOR")

@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email") or request.args.get("email")
    password = request.form.get("password") or request.args.get("password")
    if not email or not password:
        return "Email and password are required", 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO REGISTER (EMAIL, PASSWORD) VALUES (%s, %s)", (email, password))
        conn.commit()
    except mysql.connector.Error as e:
        return f"Database error: {e}", 400
    finally:
        conn.close()
    return "SUCCESS"

@app.route("/login", methods = ["POST"])
def login():
    email = request.form.get("email") or request.args.get("email")
    password = request.form.get("password") or request.args.get("password")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT email, password FROM REGISTER where email = '{email}' AND password = '{password}'")
    user = cursor.fetchone()
    conn.close()
    return "SUCCESS"

@app.route("/credentials", methods = ["POST"])
def credentials():
    email = request.form.get("email") or request.args.get("email")
    password = request.form.get("password") or request.args.get("password")
    conn = get_connection()
    cursor = conn.cursor()
    hashed = hashlib.sha1(password.encode("utf-8")).hexdigest().upper()
    cursor.execute(f"INSERT INTO CREDENTIALS VALUES('{email}', '{hashed}')")
    conn.commit()
    conn.close()
    return [email, hashed]

@app.route("/check", methods = ["GET"])
def check():
    # if "user" not in session:
    #     return redirect(url_for("login"))
    email = session.get("user", request.args.get("email", "mav@gmail.com"))
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"SELECT PASSWORD FROM CREDENTIALS WHERE EMAIL = '{email}'")
    password = cursor.fetchone()[0] or request.args.get("password")
    five = password[:5]
    later = password[5:]
    url = f"https://api.pwnedpasswords.com/range/{five}"
    res = requests.get(url)
    found = False
    for line in res.text.splitlines():
        suffix, count = line.split(":")
        if suffix.upper() == later:
            found = True
            break
    conn.close()
    if found:
        return "FOUND IN DATA BREACH. PLEASE CHANGE YOUR PASSWORD FOR ASSOCIATED ACCOUNTS"
    else:
        return "SAFE. PASSWORD NOT FOUND IN DATA BREACH"

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug = True)