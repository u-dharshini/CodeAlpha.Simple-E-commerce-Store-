from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Category, Product, Order

# ------------------ Home ------------------

@login_required
def home(request, category_id=None):
    categories = Category.objects.all()
    
    if category_id:  # If a category is selected
        products = Product.objects.filter(category_id=category_id)
    else:  # Show all products
        products = Product.objects.all()

    return render(request, 'home.html', {
        'categories': categories,
        'products': products,
        'selected_category_id': category_id,  # To highlight active category
    })

# ------------------ Auth ------------------
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login_custom.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'signup.html')

# ------------------ Cart ------------------
@login_required
def add_to_cart(request, product_id):
    cart = request.session.get('cart', {})
    cart[str(product_id)] = cart.get(str(product_id), 0) + 1
    request.session['cart'] = cart
    return redirect('cart')

@login_required
def cart(request):
    cart = request.session.get('cart', {})
    orders = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = Product.objects.get(id=product_id)
        orders.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        })
        total_price += product.price * quantity

    return render(request, 'cart.html', {'orders': orders, 'total_price': total_price})

@login_required
def remove_from_cart(request, product_id):
    cart = request.session.get('cart', {})
    if str(product_id) in cart:
        del cart[str(product_id)]
        request.session['cart'] = cart
    return redirect('cart')

# ------------------ Place Order ------------------
@login_required
def place_order(request):
    cart_items = request.session.get('cart', {})
    if not cart_items:
        messages.error(request, "Your cart is empty!")
        return redirect('cart')

    orders = []
    total_price = 0

    for product_id, quantity in cart_items.items():
        product = Product.objects.get(id=product_id)
        orders.append({
            'product': product,
            'quantity': quantity,
            'subtotal': product.price * quantity
        })
        total_price += product.price * quantity

    # Clear cart after placing order
    request.session['cart'] = {}

    return render(request, 'order_success.html', {'orders': orders, 'total_price': total_price})
