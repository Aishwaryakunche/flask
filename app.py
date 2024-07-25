from flask import Flask, render_template, request, redirect, session
import mysql.connector
from sentiments import second
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.register_blueprint(second)

# Initialize database connection and cursor
conn = None
cursor = None

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="walu",
        password="Aishubujji@123",
        database="walu"
    )
    cursor = conn.cursor()
except mysql.connector.Error as err:
    print(f"Error: {err}")
    # Consider exiting or logging the error if connection fails
    exit(1)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/home')
def home():
    if 'user_id' in session:
        return render_template('home.html')
    else:
        return redirect('/')

@app.route('/login_validation', methods=['POST'])
def login_validation():
    email = request.form.get('email')
    password = request.form.get('password')

    if cursor:
        cursor.execute(
            "SELECT * FROM users WHERE email = %s AND password = %s",
            (email, password)
        )
        users = cursor.fetchall()
        if len(users) > 0:
            session['user_id'] = users[0][0]
            return redirect('/home')
    return redirect('/')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form.get('uname')
    email = request.form.get('uemail')
    password = request.form.get('upassword')

    if cursor and conn:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password)
        )
        conn.commit()
        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            (email,)
        )
        myuser = cursor.fetchall()
        if myuser:
            session['user_id'] = myuser[0][0]
            return redirect('/home')
    return redirect('/register')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
