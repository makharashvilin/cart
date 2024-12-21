from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Category, Cart
from .forms import ProductForm
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def home(request):
    filters = dict()

    product_name = request.GET.get('product_name')
    if product_name:
        filters['name__icontains'] = product_name

    min_price = request.GET.get('min_price')
    if min_price:
        filters['price__gt'] = min_price

    max_price = request.GET.get('max_price')
    if max_price:
        filters['price__lt'] = max_price

    address = request.GET.get('address')
    if address:
        filters['address__icontains'] = address

    category =  request.GET.get('category')
    if category:
        filters['category_id'] = category


    products = Product.objects.filter(**filters)
    sort_by = request.GET.get('sort')
    if sort_by:
        products = products.order_by(sort_by)


    products_paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    try:
        page_obj = products_paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = products_paginator.page(1)
    except EmptyPage:
        page_obj = products_paginator.page(products_paginator.num_pages)



    categories = Category.objects.all()

    return render(request, 'home.html', {'products': page_obj,
                                                                'products_paginator':products_paginator,
                                                              'categories': categories})


def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    product.views+=1
    product.save()
    return render(request, 'product_detail.html', {'product': product})


def create_product(request):
    form = ProductForm()
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Form submitted successfully.')
        return redirect('home')
    return render(request, 'product_form.html', {'form':form})



def update_product(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f'Product {product.name} Has Been Updated Successfully.')
            return redirect('product_detail', id=product.id)
    else:
        form = ProductForm(instance=product)
        return render(request, 'update_product.html', {'form': form, 'product': product})


def delete_product(request, id):
    product = get_object_or_404(Product, id=id)
    product_name = product.name
    product.delete()
    messages.success(request, f"Product {product_name} has been deleted.")
    return redirect('home')



def cart_view(request):
    cart, created = Cart.objects.get_or_create(user_id=request.user.id)
    return render(request, 'cart.html', {'cart':cart})


def add_product_to_cart(request, id):
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = Product.objects.get(id=id)
    cart.products.add(product)
    cart.save()


    return redirect('product_detail', id=id)






