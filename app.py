from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///account.db'
db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    wallet_address = db.Column(db.String(42), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        wallet_address = request.form['wallet_address']
        password = request.form['password']
        user = User.query.filter_by(wallet_address=wallet_address, password=password).first()
        if user:
            session['user_id'] = user.id
            session['wallet_address'] = user.wallet_address
            return redirect(url_for('dashboard'))
        else:
            return "Invalid credentials. \nPlease check your address and password. \nPlease also make sure you have registered."
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        wallet_address = request.form['wallet_address']
        password = request.form['password']
        new_user = User(wallet_address=wallet_address, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/create_project', methods=['GET', 'POST'])
def create_project():
    if 'wallet_address' not in session:
        return redirect(url_for('login'))
    return render_template('create_project.html', wallet_address=session['wallet_address'])

@app.route('/view_projects', methods=["GET", "POST"])
def view_projects():
    return render_template('view_projects.html')

@app.route('/my_projects', methods=["GET", "POST"])
def my_projects():
    if 'wallet_address' not in session:
        return redirect(url_for('login'))
    return render_template('my_projects.html', wallet_address=session['wallet_address'])

@app.route('/donate/<int:project_id>', methods=["GET", "POST"])
def donate(project_id):
    return render_template('donate.html', project_id=project_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
