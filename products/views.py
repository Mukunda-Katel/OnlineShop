from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Category
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.contrib import messages
# Create your views here.
def home(request):
    products = Product.objects.filter(avilable=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    context= {
        'products':products,
        'categories': categories,
    }
    return render(request, '', context)


@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            messages.success(request,"Product added successfully")
            return redirect('')
    else:
        form = ProductForm()
    return render()
    

@login_required  
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk, seller = request.user)
    if request.method=='POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request,"Product updated successfully")
            return redirect()
    else:
        form = ProductForm(instance=product)
    return render()