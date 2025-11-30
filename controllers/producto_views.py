from flask import Blueprint, render_template, request, redirect, url_for
from model.producto import Producto
from model.db import db

# Crear el blueprint para las vistas de productos
producto_views = Blueprint('producto_views', __name__)

# Mostrar la lista de productos
@producto_views.route('/productos')
def producto_list():
    productos = Producto.query.all()
    return render_template('producto_list.html', productos=productos)

# Mostrar el formulario para crear un nuevo producto
@producto_views.route('/productos/create', methods=['GET'])
def producto_create():
    return render_template('producto_create.html')

# Crear un nuevo producto desde el formulario
@producto_views.route('/productos/create', methods=['POST'])
def create_producto_post():
    nombre = request.form['nombre']
    descripcion = request.form['descripcion']
    precio = request.form['precio']

    nuevo_producto = Producto(nombre=nombre, descripcion=descripcion, precio=precio)
    db.session.add(nuevo_producto)
    db.session.commit()

    return redirect(url_for('producto_views.producto_list'))  # Redirigir a la lista de productos

# Mostrar los detalles de un producto específico
@producto_views.route('/productos/<int:id>')
def producto_detail(id):
    producto = Producto.query.get_or_404(id)
    return render_template('producto_detail.html', producto=producto)

# Mostrar el formulario para editar un producto
@producto_views.route('/productos/<int:id>/edit', methods=['GET'])
def producto_edit(id):
    producto = Producto.query.get_or_404(id)
    return render_template('producto_edit.html', producto=producto)

# Actualizar un producto desde el formulario
@producto_views.route('/productos/<int:id>/edit', methods=['POST'])
def update_producto_post(id):
    producto = Producto.query.get_or_404(id)

    producto.nombre = request.form['nombre']
    producto.descripcion = request.form['descripcion']
    producto.precio = request.form['precio']
    
    db.session.commit()

    return redirect(url_for('producto_views.producto_list'))  # Redirigir a la lista de productos

# Eliminar un producto
@producto_views.route('/productos/<int:id>/delete', methods=['POST'])
def delete_producto(id):
    producto = Producto.query.get_or_404(id)
    db.session.delete(producto)
    db.session.commit()

    return redirect(url_for('producto_views.producto_list'))  # Redirigir a la lista de productos
