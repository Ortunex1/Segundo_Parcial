from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "clave_secreta"

# Inicializamos la variable current_id en 1, que incrementará con cada nuevo producto
current_id = 1

@app.route('/')
def index():
    # Si no hay productos en la sesión, inicializamos una lista vacía
    if 'products' not in session:
        session['products'] = []

    # Obtenemos los productos de la sesión
    products = session['products']
    return render_template('index.html', products=products)

@app.route('/add', methods=['POST'])
def add_product():
    global current_id  # Usamos la variable global current_id

    # Creamos el nuevo producto con el ID que se incrementa automáticamente
    new_product = {
        'id': current_id,  # ID numérico secuencial
        'nombre': request.form['nombre'],
        'cantidad': int(request.form['cantidad']),
        'precio': float(request.form['precio']),
        'fecha_vencimiento': request.form['fecha_vencimiento'],
        'categoria': request.form['categoria']
    }

    # Incrementamos el ID para el siguiente producto
    current_id += 1

    # Agregamos el nuevo producto a la lista de productos en la sesión
    products = session.get('products', [])
    products.append(new_product)
    session['products'] = products

    return redirect(url_for('index'))

@app.route('/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    products = session.get('products', [])

    # Buscar el producto por ID
    product = next((prod for prod in products if prod['id'] == product_id), None)

    if request.method == 'POST':
        # Actualizamos los datos del producto
        product['nombre'] = request.form['nombre']
        product['cantidad'] = int(request.form['cantidad'])
        product['precio'] = float(request.form['precio'])
        product['fecha_vencimiento'] = request.form['fecha_vencimiento']
        product['categoria'] = request.form['categoria']

        session['products'] = products
        return redirect(url_for('index'))

    return render_template('edit.html', product=product)

@app.route('/delete/<int:product_id>')
def delete_product(product_id):
    products = session.get('products', [])

    # Filtramos el producto a eliminar
    products = [prod for prod in products if prod['id'] != product_id]
    session['products'] = products

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
