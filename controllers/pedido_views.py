from flask import Blueprint, jsonify, render_template, request, redirect, url_for
from model.pedido import Pedido
from model.producto import Producto
from model.cliente import Cliente
from model.db import db

# Crear el blueprint para las vistas de pedidos
pedido_views = Blueprint('pedido_views', __name__)

# Mostrar la lista de pedidos
@pedido_views.route('/pedidos')
def pedido_list():
    pedidos = Pedido.query.all()
    return render_template('pedido_list.html', pedidos=pedidos)

# Mostrar el formulario para crear un nuevo pedido
@pedido_views.route('/pedidos/create', methods=['GET'])
def pedido_create():
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    return render_template('pedido_create.html', clientes=clientes, productos=productos)

# Crear un nuevo pedido desde el formulario
@pedido_views.route('/pedidos/create', methods=['POST'])
def create_pedido_post():
    cliente_id = request.form['cliente_id']
    producto_ids = request.form.getlist('producto_ids')  # Obtener los productos seleccionados
    
    # Obtener los productos seleccionados
    productos = Producto.query.filter(Producto.id.in_(producto_ids)).all()

    if not productos:
        return jsonify({"error": "No se encontraron productos válidos."}), 404

    # Crear el pedido y asociar los productos
    nuevo_pedido = Pedido(cliente_id=cliente_id)
    nuevo_pedido.productos = productos  # Asegurarse de asociar los productos correctamente

    # Calcular el total del pedido
    nuevo_pedido.calcular_total()
    
    db.session.add(nuevo_pedido)
    db.session.commit()

    return redirect(url_for('pedido_views.pedido_list'))  # Redirigir a la lista de pedidos


# Mostrar los detalles de un pedido específico
@pedido_views.route('/pedidos/<int:id>')
def pedido_detail(id):
    pedido = Pedido.query.get_or_404(id)
    return render_template('pedido_detail.html', pedido=pedido)

# Mostrar el formulario para editar un pedido
@pedido_views.route('/pedidos/<int:id>/edit', methods=['GET'])
def pedido_edit(id):
    pedido = Pedido.query.get_or_404(id)
    clientes = Cliente.query.all()
    productos = Producto.query.all()
    return render_template('pedido_edit.html', pedido=pedido, clientes=clientes, productos=productos)

# Actualizar un pedido desde el formulario
@pedido_views.route('/pedidos/<int:id>/edit', methods=['POST'])
def update_pedido_post(id):
    pedido = Pedido.query.get_or_404(id)

    # Actualizar los datos del pedido
    pedido.cliente_id = request.form['cliente_id']
    producto_ids = request.form.getlist('producto_ids')
    productos = Producto.query.filter(Producto.id.in_(producto_ids)).all()

    if not productos:
        return jsonify({"error": "No se encontraron productos válidos."}), 404

    pedido.productos = productos
    pedido.calcular_total()  # Recalcular el total del pedido

    db.session.commit()

    return redirect(url_for('pedido_views.pedido_list'))  # Redirigir a la lista de pedidos

# Eliminar un pedido
@pedido_views.route('/pedidos/<int:id>/delete', methods=['POST'])
def delete_pedido(id):
    pedido = Pedido.query.get_or_404(id)
    db.session.delete(pedido)
    db.session.commit()

    return redirect(url_for('pedido_views.pedido_list'))  # Redirigir a la lista de pedidos
