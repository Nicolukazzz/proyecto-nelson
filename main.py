from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///productos.db'
app.config['SECRET_KEY'] = 'your_secret_key'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


productos = {}
producto_id = 1

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
@login_required
def index():
    return render_template('index.html', productos=productos)

@app.route('/add', methods=['POST'])
@login_required
def add_producto():
    global producto_id
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    ubicacion = request.form['ubicacion']
    fecha_de_vencimiento = request.form['fecha_de_vencimiento']
    precio = request.form['precio']
    productos[producto_id] = {'nombre': nombre, 'cantidad': cantidad, 'ubicacion': ubicacion, 'fecha_de_vencimiento': fecha_de_vencimiento ,'precio': precio}
    producto_id += 1
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_producto(id):
    if request.method == 'POST':
        productos[id]['nombre'] = request.form['nombre']
        productos[id]['cantidad'] = request.form['cantidad']
        productos[id]['ubicacion'] = request.form['ubicacion']
        productos[id]['fecha_de_vencimiento'] = request.form['fecha_de_vencimiento']
        productos[id]['precio'] = request.form['precio']
        return redirect(url_for('index'))
    return render_template('edit.html', id=id, producto=productos[id])

@app.route('/delete/<int:id>', methods=['POST'])
@login_required
def delete_producto(id):
    if id in productos:
        del productos[id]
    return redirect(url_for('index'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        print('Usuario registrado', username, password)
        return redirect(url_for('login'))
    return render_template('register.html')
    


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 3000)))