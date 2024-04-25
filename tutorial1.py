from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

# Homepage
@app.route('/')
def home():
    return "Hello, this is the main page <h1>HELLO</h1>"


@app.route('/<name>')
def user(name):
    return f"Hello {name}!"

@app.route('/admin')
def admin():
    # return redirect(url_for('home')) #home is the function name.
    return redirect(url_for('user',name='Admin!!!')) #user is the function name. redirect to this function.

if __name__ == '__main__':
    app.run(port=8080)