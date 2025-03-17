from flask import Flask, jsonify, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# A user must have one of the following roles
ADMIN = 'admin'.casefold()
ALTUSER = 'altuser'.casefold()
USER = 'user'.casefold()
roles = [
    ADMIN,
    ALTUSER,
    USER
    ]

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)

# Create the database tables. This must come after all model declarations.
with app.app_context():
    db.create_all()

@app.route('/')
def root():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['username'] = user.username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
        return render_template('login.html'), 401
    return render_template('login.html')

@app.route('/altlogin', methods=['GET', 'POST'])
def altlogin():
    if 'user_id' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
        return render_template('altlogin.html'), 401
    return render_template('altlogin.html')

@app.route('/jsonlogin', methods=['GET', 'POST'])
def jsonlogin():
    if 'user_id' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        data = request.get_json()
        if data:
            username = data['username']
            password = data['password']
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['role'] = user.role
                flash('Login successful!', 'success')
                return jsonify({'message':'Login successful'})
            return jsonify({'message':'Invalid credentials'}), 401
        return jsonify({'message':'Unable to read JSON payload'}), 500
    return render_template('jsonlogin.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login')), 401
    role = session.get('role')
    username = session.get('username')
    if role == ADMIN:
        return render_template('admin_dashboard.html', username=username)
    return render_template('user_dashboard.html', username=username)

@app.route('/altuser')
def altuser():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login')), 401
    role = session.get('role')
    username = session.get('username')
    if role in [ADMIN, ALTUSER]:
        return render_template('altuser.html', username=username)
    return render_template('forbidden.html', username=username), 403

@app.route('/user')
def user():
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login')), 401
    role = session.get('role')
    username = session.get('username')
    if role in [ADMIN, USER]:
        return render_template('altuser.html', username=username)
    return render_template('forbidden.html', username=username), 403

@app.route('/admin')
def admin():
    if session.get('role') != ADMIN:
        flash('Access denied!', 'danger')
        return redirect(url_for('dashboard')), 403
    return render_template('admin_dashboard.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('dashboard'))
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        role = request.form['role']
        if role.casefold()  not in roles:
            flash(f'{role}: invalid role (must be one of {", ".join(roles)})', 'danger')
            return render_template('register.html'), 400
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.before_request
def log_request_info():
    app.logger.debug(f'Request method: {request.method}')
    app.logger.debug(f'Request headers: {request.headers}')
    if request.method == 'POST':
        app.logger.debug(f'Request body: {request.get_data()}')

@app.after_request
def log_response_info(response):
    app.logger.debug(f'Response headers: {response.headers}')
    app.logger.debug(f'Response body: {response.get_data()}')
    return response

if __name__ == '__main__':
    with app.app_context():
        create_tables()
        app.run(debug=True)
