import sqlite3
from unicodedata import name
from django.db import connection
from flask import Flask, render_template, request
import psycopg2
import psycopg2.extras


app = Flask(__name__)
app.secret_key = 'cairocoders-ednalan'
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


DB_HOST = "ec2-3-225-213-67.compute-1.amazonaws.com"
DB_NAME = "d6sn9ub73sh1i1"
DB_USER = "owfyzwdyexiqpt"
DB_PASS = "a7b9d3d9608ddbcf3ca830ae5dce5d6f2f791fc2040c810ec9954232f0b7693f"

conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
mycursor =conn.cursor()

@app.route("/", methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/account', methods=['GET', 'POST'])
def signup():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST' and 'username' and 'idnum' and 'email' and 'password' and 'cpassword':
        username = request.form['username']
        idnum = request.form['idnum']
        email = request.form['email']
        password = request.form['password'] 
        cpassword = request.form['cpassword']

        _hashed_password = generate_password_hash(password)

        #Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE nic = %s', (idnum,))
        account = cursor.fetchone()
        print(account)
        # If account exists show error and validation checks
        if account:
            flash('Account already exists!')
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', nic):
            flash('Username must contain only characters and numbers!')
        elif not nic or not password or not email:
            flash('Please fill out the form!')
        else:
            cursor.execute("INSERT INTO users (username, email, idnum, password, cpassword ) VALUES (%s,%s,%s,%s,%s)", (firstName,lastName, nic,phonenumber, email,password,confirmPassword))
            conn.commit()
            flash('You have successfully registered!')
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        flash('Please fill out the form!')
    # Show registration form with message (if any)
    return render_template('account.html')



@app.route('/account', methods=['GET', 'POST'])
def login():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        print(password)
        # Check if account exists using MySQL
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        # Fetch one record and return result
        account = cursor.fetchone()

        if account:
            password_rs = account['password']
            print(password_rs)
            # If account exists in users table in out database
            if check_password_hash(password_rs, password):
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['id']
                session['email'] = account['username']
                # Redirect to home page
                return redirect(url_for('/'))
            else:
                # Account doesnt exist or username/password incorrect
                flash('Incorrect email/password')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect email/password')
    return render_template('account.html')

@app.route("/earth", methods=['GET'])
def earth():
    return render_template('earth.html')

@app.route("/moon", methods=['GET'])
def moon():
    return render_template('moon.html')

@app.route("/mars", methods=['GET'])
def mars():
    return render_template('mars.html')
    
@app.route("/admin", methods=['GET'])
def admin():
    return render_template('admin.html')

if __name__ == '__main__':
   app.run(debug=True)