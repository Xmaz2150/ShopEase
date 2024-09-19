from typing import cast

from flask import jsonify, request, redirect, url_for
from models import storage
from utils.file import upload_file, rename_file
from config.settings import Config
from datetime import datetime
from models.models import BaseModel, Product, Category, Cart, CartItem, Order, OrderItem
from views import shop_views
from flask_jwt_extended import jwt_required, get_jwt, current_user
from views.helpers import role_required

PRODUCT_CATEGORIES = [
    'Clothing',
    'Shoes',
    'Electronics',
    'Books',
    'Games',
    'Beauty_Health',
    'Food_And_Beverage',
    'Hand_Bags',
    'Jewellery_And_Accessories',
    'Home_And_Gifts'
]

@shop_views.route('/products', methods=['GET'])
@jwt_required(optional=True)
def get_products():
    ''' Gets all the users by category all if not specified '''
    data = request.get_json()
    category = data.get('category')

    if not category:
        return jsonify({"message": "Invalid data!"}), 400

    products = [p.to_dict() for key, p in storage.all(Product, category).items()]

    if category == 'ALL':
        return jsonify({ 'All products': products})
    elif category not in PRODUCT_CATEGORIES:
        return jsonify({"message": "Invalid category!"}), 400

    return jsonify({ category: products})

@shop_views.route('/product', methods=['POST'])
@jwt_required()
@role_required('admin')
def upload_product():
    ''' Adds new productus to database '''
    file = request.files['file']
    name = request.form.get('name')
    description = request.form.get('description')
    price = request.form.get('price')
    brand = request.form.get('brand')
    stock_quantity = request.form.get('stock_quantity')
    category = request.form.get('category')

    if not name or not description or not price \
        or not brand or not stock_quantity \
        or not category:
        return jsonify({"message": "Invalid data!"}), 400

    if category not in PRODUCT_CATEGORIES:
        return jsonify({"message": "Invalid category!"}), 400

    p_category = [c for key, c in storage.all(Category).items() if c.name == category][0]
    new_product = Product(
        name = name,
        description=description,
        price=float(price),
        brand=brand,
        stock_quantity=int(stock_quantity),
        category_id=p_category.id
    )

    image_name = upload_file(file)
    new_product.image_url = image_name
    new_product.save()
    
    ''' Workaround to make image_url saveable with correct url'''
    product_update = storage.get(Product, id=new_product.id)
    url_prefix = Config.IMG_URL_PREFIX
    product_update.image_url = '{}{}.{}'.format(url_prefix, new_product.id, image_name)
    rename_file(image_name, '{}.{}'.format(new_product.id, image_name))
    product_update.save()


    return jsonify({
        'id': new_product.id,
        'name': new_product.name,
        'image_url': product_update.image_url
    }), 201


@shop_views.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    ''' Gets all items in cart for specific user '''
    cart = storage.get(Cart, user_id=current_user.id)
    if not cart:
        return jsonify({"message": "Error loading cart!"}), 404
    
    cart_items = [p.to_dict() for key, p in storage.all(CartItem, None, cart_id=cart.id).items()]
    print(cart_items)
    return jsonify({'Cart': cart_items})

@shop_views.route('/cart/add', methods=['POST'])
@jwt_required()
def add_to_cart():
    ''' Gets all items in cart for specific user '''
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    if not product_id or not quantity:
        return jsonify({"message": "Invalid data!"}), 400

    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"message": "Invalid data(quantity)!"}), 400

    cart = storage.get(Cart, user_id=current_user.id)
    if not cart:
        cart = Cart(user_id=current_user.id)
        cart.save()
    
    product = storage.get(Product, id=product_id)
    if not product:
        return jsonify({"message": "Product does not exist!"}), 400

    cart_item = storage.get(CartItem, product_id=product_id)
    quantity = int(quantity)
    if not cart_item:
        new_item = CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity,
            price=product.price
        )
        new_item.save()
        return jsonify(new_item.to_dict()), 201
    
    if hasattr(cart_item, 'quantity') and hasattr(cart_item, 'save') \
        and hasattr(cart_item, 'to_dict'):
        cart_item.quantity += quantity
        cart_item.save() 
        return jsonify(cart_item.to_dict()), 201
    
    return jsonify({"message": "Could not add item to cart!"}), 400

@shop_views.route('/cart/remove', methods=['POST'])
@jwt_required()
def remove_from_cart():
    ''' Removes item(s) in cart for specific user '''
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity')
    
    if not product_id or not quantity:
        return jsonify({"message": "Invalid data!"}), 400

    try:
        quantity = int(quantity)
    except ValueError:
        return jsonify({"message": "Invalid data(quantity)!"}), 400

    cart = storage.get(Cart, user_id=current_user.id)
    if not cart:
        cart = Cart(user_id=current_user.id)
    
    product = storage.get(Product, id=product_id)
    if not product:
        return jsonify({"message": "Product does not exist!"}), 400

    cart_item = storage.get(CartItem, product_id=product_id)
    quantity = int(quantity)
    if not cart_item:
        return jsonify({"message": "Item does not exist in cart!"}), 400
    
    
    current_quantity = cart_item.quantity
    if current_quantity == 0:
        return jsonify({"message": "Cart is empty!"}), 400
    elif quantity >= current_quantity:
        cart_item.quantity = 0
        storage.delete(cart_item) ##
    elif quantity < 0:
        pass
    else:
        cart_item.quantity -= quantity

    cart_item.save()

    return jsonify(cart_item.to_dict()), 200

@shop_views.route('/checkout', methods=['GET'])
@jwt_required()
def checkout():
    ''' Completes purchase and creates order'''
    cart = storage.get(Cart, user_id=current_user.id)
    if not cart:
        return jsonify({"message": "Error loading cart!"}), 404
    
    cart_items = storage.all(CartItem, None, cart_id=cart.id)
    if not cart_items:
        return jsonify({"message": "Cart is empty!"}), 400
    
    new_order = Order(
        user_id=current_user.id,
        order_date=datetime.now().isoformat(),
        total_price=0
    )
    new_order.save()
    total_price = 0

    for key, item in cart_items.items():
        product = storage.get(Product, id=item.product_id)
        if not product:
            continue
        new_order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        total_price += item.price * item.quantity
        new_order_item.save()
    
    new_order.total_price = total_price
    new_order.save()
    storage.delete(cart)
    storage.save()

    return jsonify(new_order.to_dict()), 201

@shop_views.route('/orderhistory', methods=['GET'])
@jwt_required()
def order_history():
    ''' Gets all orders for specific user '''
    orders = storage.all(Order, None, current_user=current_user.id)
    if not orders:
        return jsonify({"message": "No orders found!"}), 404
    
    orders = [p.to_dict() for key, p in orders.items()]
    return jsonify({'Orders': orders}), 200
