from flask import Blueprint, render_template, request, redirect, url_for
from model.cliente import Cliente
from model.db import db

# Crear el blueprint para las vistas de clientes
cliente_views = Blueprint('cliente_views', __name__)

# Mostrar la lista de clientes
@cliente_views.route('/clientes')
def cliente_list():
    clientes = Cliente.query.all()
    return render_template('cliente_list.html', clientes=clientes)

# Mostrar el formulario para crear un nuevo cliente
@cliente_views.route('/clientes/create', methods=['GET'])
def cliente_create():
    return render_template('cliente_create.html')

# Crear un nuevo cliente desde el formulario
@cliente_views.route('/clientes/create', methods=['POST'])
def create_cliente_post():
    nombre = request.form['nombre']
    email = request.form['email']

    nuevo_cliente = Cliente(nombre=nombre, email=email)
    db.session.add(nuevo_cliente)
    db.session.commit()

    return redirect(url_for('cliente_views.cliente_list'))  # Redirigir a la lista de clientes

# Mostrar los detalles de un cliente específico
@cliente_views.route('/clientes/<string:id>')
def cliente_detail(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('cliente_detail.html', cliente=cliente)

# Mostrar el formulario para editar un cliente
@cliente_views.route('/clientes/<string:id>/edit', methods=['GET'])
def cliente_edit(id):
    cliente = Cliente.query.get_or_404(id)
    return render_template('cliente_edit.html', cliente=cliente)

# Actualizar un cliente desde el formulario
@cliente_views.route('/clientes/<string:id>/edit', methods=['POST'])
def update_cliente_post(id):
    cliente = Cliente.query.get_or_404(id)

    cliente.nombre = request.form['nombre']
    cliente.email = request.form['email']
    
    db.session.commit()

    return redirect(url_for('cliente_views.cliente_list'))  # Redirigir a la lista de clientes

# Eliminar un cliente
@cliente_views.route('/clientes/<string:id>/delete', methods=['POST'])
def delete_cliente(id):
    cliente = Cliente.query.get_or_404(id)
    db.session.delete(cliente)
    db.session.commit()

    return redirect(url_for('cliente_views.cliente_list'))  # Redirigir a la lista de clientes
