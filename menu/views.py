from django.shortcuts import render, get_object_or_404, redirect
from .models import Pricing, Product
from .forms import PricingForm, ProductForm
from django.contrib.auth.decorators import login_required


@login_required('account:login')
def product_list(request):
    products = Product.objects.all()
    return render(request, '', {'products': products})

@login_required('account:login')
def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, '', {'product': product})

@login_required('account:login')
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm

    return render(request, 'menu/add_product.html', {'form': form})
        
@login_required('account:login')
def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            return redirect('product_detail', product_id=product.id)
    else:
        form = ProductForm(instance=product)

    return render(request, 'menu/update_product.html', {'form': form, 'product': product})

@login_required('account:login')
def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    product.delete()

@login_required('account:login')
def pricing_list(request):
    pricings = Pricing.objects.all()
    return render(request, 'menu/pricing_list.html', {'pricings': pricings})

@login_required('account:login')
def pricing_detail(request, pricing_id):
    pricing = get_object_or_404(Pricing, pk=pricing_id)
    return render(request, 'menu/pricing_detail.html', {'pricing': pricing})

@login_required('account:login')
def add_pricing(request):
    if request.method == 'POST':
        form = PricingForm(request.POST)
        if form.is_valid():
            pricing = form.save()
            return redirect('pricing_detail', pricing_id=pricing.id)
    else:
        form = PricingForm()

    return render(request, 'menu/add_pricing.html', {'form': form})

@login_required('account:login')
def update_pricing(request, pricing_id):
    pricing = get_object_or_404(Pricing, pk=pricing_id)

    if request.method == 'POST':
        form = PricingForm(request.POST, instance=pricing)
        if form.is_valid():
            form.save()
            return redirect('pricing_detail', pricing_id=pricing.id)
    else:
        form = PricingForm(instance=pricing)

    return render(request, 'menu/update_pricing.html', {'form': form, 'pricing': pricing})

@login_required('account:login')
def delete_pricing(request, pricing_id):
    pricing = get_object_or_404(Pricing, pk=pricing_id)
    pricing.delete()
    return redirect('pricing_list')