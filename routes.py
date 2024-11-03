from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
from models import db, User, Product  # Đảm bảo rằng bạn đã định nghĩa các mô hình này

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/products')
def products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/cart')
@login_required
def cart():
    # Logic to display items in cart
    return render_template('cart.html')

@app.route('/admin_dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    products = Product.query.all()
    return render_template('admin_dashboard.html', products=products)

@app.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not current_user.is_admin:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        try:
            name = request.form['name']
            description = request.form['description']
            price = float(request.form['price'])
            category = request.form['category']
            
            product = Product(name=name, description=description, price=price, category=category)
            db.session.add(product)
            db.session.commit()
            flash('Product added successfully.')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()  # Hoàn tác nếu có lỗi
            flash(f'An error occurred: {e}')
    
    return render_template('add_product.html')

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    # Ensure only admins can access this route
    if not current_user.is_admin:
        flash('Access denied.')
        return redirect(url_for('home'))
    
    # Get the product by ID
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        # Update product details from form data
        try:
            product.name = request.form['name']
            product.description = request.form['description']
            product.price = float(request.form['price'])
            product.category = request.form['category']
            
            # Commit changes to the database
            db.session.commit()
            flash('Product updated successfully.')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            db.session.rollback()  # Hoàn tác nếu có lỗi
            flash(f'An error occurred: {e}')
    
    # Render edit page with current product details
    return render_template('edit_product.html', product=product)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful. Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)
