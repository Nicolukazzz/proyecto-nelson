from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

productos = {}
producto_id = 1

@app.route('/')
def index():
    return render_template('index.html', productos=productos)

@app.route('/add', methods=['POST'])
def add_producto():
    global producto_id
    nombre = request.form['nombre']
    cantidad = request.form['cantidad']
    ubicacion = request.form['ubicacion']
    precio = request.form['precio']
    productos[producto_id] = {'nombre': nombre, 'cantidad': cantidad, 'ubicacion': ubicacion, 'precio': precio}
    producto_id += 1
    return redirect(url_for('index'))

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_producto(id):
    if request.method == 'POST':
        productos[id]['nombre'] = request.form['nombre']
        productos[id]['cantidad'] = request.form['cantidad']
        productos[id]['ubicacion'] = request.form['ubicacion']
        productos[id]['precio'] = request.form['precio']
        return redirect(url_for('index'))
    return render_template('edit.html', id=id, producto=productos[id])

@app.route('/delete/<int:id>')
def delete_producto(id):
    if id in productos:
        del productos[id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()