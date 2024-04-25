from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="my_flask_website",
    user="postgres",
    password="P@ssW0rd",
    port="5432")

cur = conn.cursor()


app = Flask(__name__)
app.secret_key = "hello" # Secret key for the session
app.permanent_session_lifetime = timedelta(minutes=5) # Set the (permament) session to last for 5 minutes


@app.route('/')
def home():
    # return render_template("index.html",content=name,r=2)
    return render_template("index.html")


@app.route('/login',methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True # Set the session to be permanent (last for 5 minutes)
        
        user = request.form['nm']
    
        # Store the user in a session
        session['user'] = user

        flash(f"Login successful! Welcome, {user}!", "info")

        return redirect(url_for('user'))
    else:
        if 'user' in session:
            flash("Already logged in!", "info")
            return redirect(url_for('user'))
        return render_template('login.html')


@app.route('/user', methods=['POST', 'GET'])
def user():
    email = None

    if 'user' in session:
        user = session['user'] # Get the user from the session

        if request.method == 'POST':
            email = request.form['email']
            session['email'] = email
            

            # Save email to the database
            try:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS emails (
                        id SERIAL PRIMARY KEY,
                        user_email VARCHAR(255) NOT NULL
                    )
                """)
                conn.commit()
                cur.execute("INSERT INTO emails (user_email) VALUES (%s)", (email,))
                conn.commit()
                flash("Email was saved!")
            except psycopg2.Error as e:
                conn.rollback()
                flash(f"Error saving email: {e}", "error")
        else:
            if 'email' in session:
                email = session['email']

        return render_template('user.html', email=email)
    else:
        flash("You are not logged in!", "info")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    if 'user' in session:
        user = session['user'] # Get the user from the session
        flash(f"You have been logged out, {user}!", "info") # flash a message to the user. info is the category of the message.

    session.pop('user',None) # Remove the user from the session
    session.pop('email',None)

    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(port=8080,debug=True)