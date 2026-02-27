from flask import Flask, render_template, request, redirect, session, url_for
import bcrypt
import mysql.connector

app = Flask(__name__)
app.secret_key = "password"

def get_connection():
    return mysql.connector.connect(host = "localhost", user = "root", password = "", database = "MONITOR")

@app.route("/register", methods = ["POST"])
def register():
    email = request.form["email"]
    password = request.form["password"]
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(f"INSERT INTO REGISTER VALUES('{email}', '{password}')")
    conn.commit()
    conn.close()
    return redirect(url_for("login"))

@app.route("/login", methods = ["POST"])
def login():
    pass

@app.route("/credentials", methods = ["POST"])
def credentials():
    pass

@app.route("/check", methods = ["GET"])
def check():
    pass

@app.route("/logout")
def logout():
    pass

if __name__ == "__main__":
    app.run(debug = True)