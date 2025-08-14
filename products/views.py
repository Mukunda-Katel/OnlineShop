from django.shortcuts import render, redirect, get_object_or_404
from .models import Product,Category
from django.contrib.auth.decorators import login_required
from .forms import ProductForm
from django.contrib import messages
from django.db.models import Q



# Create your views here.
def home(request):
    products = Product.objects.filter(avilable=True).order_by('-created_at')[:8]
    categories = Category.objects.all()
    context= {
        'products':products,
        'categories': categories,
    }
    return render(request, '',context)


def product_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    
    products = Product.objects.filter(avilable=True)
    
    if query:
        products = products.filter(
            Q(name__icontain=query) |
            Q(description__icontain=query) |
            Q(seller__username__icontain=query)
            
        )
    if category_id:
        products= products.filter(category_id=category_id)
        
    products = products.order_by('-created_at')
    
    paginator = paginator(products, 12)
    page_number= request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    
    categories = Category.objects.all()
    
    context = {
        'page_obj':page_obj,
        'categories':categories,
        'query':query,
        'selected_category':int(category_id) if category_id else None,
        
    }
    return render(request,'' ,context)
    
    
    
    # 127.0.0.1/products/12
    










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


def delete_product(request, pk):
    product= get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'delete bhayo')
        return redirect()
    return render()