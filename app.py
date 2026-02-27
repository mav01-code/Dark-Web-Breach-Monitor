from flask import Flask, render_templates, request, redirect, session, url_for
import bycrypt
import mysql.connector

app = Flask(__name__)

def get_connection():
    return mysql.connector.connect(host = "localhost", user = "root", password = "Varsini@102006", database = "MONITOR")

def register():
    pass

def login():
    pass

def dashboard():
    pass

def logout():
    pass

if __name__ == "__main__":
    app.run(debug = True)