from django.shortcuts import render,get_object_or_404,redirect
from . models import *
from django.contrib.auth.models import User
from shop.forms import customform
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout 
from django.contrib.auth.decorators import login_required

def home(request):
    trending_products = products.objects.filter(trending=1)
    return render(request,'shop/home.html',{'trending_products':trending_products})

def register(request):
    forms = customform()
    if request.method == 'POST':
        forms = customform(request.POST)
        if forms.is_valid():
            forms.save()
            messages.success(request, "Your account has been created successfully.")
            return redirect("login")  
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        forms = customform()
        
    return render(request,'shop/register.html',{'forms':forms})

def logout_page(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"logout successfully")
    return redirect('/')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            name = request.POST.get('username')
            pwd = request.POST.get('password')
            user = authenticate(request,username=name,password=pwd)
            if user is not None:
                login(request,user)
                messages.success(request,"Logged in successfully")
                return redirect('/')
            else:
                messages.error(request,"Username or Password wrong")
                return redirect('login')
    return render(request,'shop/login.html')

def collections(request):
    categories_collections = Category.objects.filter(status=0)
    return render(request,'shop/collections.html',{'categories_collections':categories_collections})

def category_products(request, cat_id):
    category_variable= get_object_or_404(Category, id=cat_id)
    category_products = products.objects.filter(category=category_variable, status=0)
    return render(request, 'shop/category_products.html', {
        'category': category_variable,
        'products': category_products
    })

def product_view(request,pro_id):
    one_product = get_object_or_404(products,id=pro_id)
    similar_product = products.objects.filter(category=one_product.category, status=0).exclude(id=pro_id)
    return render(request,'shop/product_view.html',{'one_product':one_product , 'similar_product':similar_product})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(products, id=product_id)
    
    # Already cart-la irukka check pannuthu
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    return redirect('cart_view')

@login_required
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = 0
    for item in cart_items:
        total += item.total_price()
    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total': total})

@login_required
def remove_from_cart(request, cart_id):
    cart_item = get_object_or_404(Cart, id=cart_id, user=request.user)
    cart_item.delete()
    return redirect('cart_view')  # redirect back to cart page

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    total = sum([item.total_price() for item in cart_items])

    if request.method == 'POST' and cart_items.exists():
        # Create Order
        order = Order.objects.create(user=request.user, total_price=total)

        # Create OrderItems
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.selling_price,
                customer_name =request.POST.get('name'),
                phone = request.POST.get('phone'),
                address = request.POST.get('address')
            )

        # Clear Cart
        cart_items.delete()

        messages.success(request, "Your order has been placed successfully!")
        return render(request, 'shop/checkout_success.html', {'order': order})

    return render(request, 'shop/checkout.html', {'cart_items': cart_items, 'total': total})

