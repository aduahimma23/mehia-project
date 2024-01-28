from django.shortcuts import render, get_object_or_404, get_list_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Sum
from orders.models import Order
from .models import *
from .forms import FoodVendorForm

@login_required(login_url='account:login')
def vendor_list(request):
    vendors = FoodVendor.objects.all()
    return render(request, 'vendor/vendor_list.html', {'vendors': vendors})

@login_required(login_url='account:login')
def vendor_details(request, vendor_id):
    vendor = get_list_or_404(FoodVendor, pk=vendor_id)
    orders_today = Order.objects.filter(vendor=vendor, date_ordered__date=timezone.now())
    total_amount_received = orders_today.aggregate(Sum('amount_received'))['amount_received__sum'] or 0
    return render(request, 'foodapp/vendor_detail.html', {'vendor': vendor, 'orders_today': orders_today, 'total_amount_received': total_amount_received})

@login_required(login_url='account:login')
def update_vendor(request, vendor_id):
    vendor = get_list_or_404(FoodVendor, pk=vendor_id)

    if request.method == 'POST':
        form = FoodVendorForm(request.POST, request.FILES, instance=vendor)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = FoodVendorForm(instance=vendor)

    return render(request, 'vendor/update_vendor.html', {'form': form, 'vendor': vendor})

@login_required(login_url='account:login')
def add_vendor(request):
    if request.method == 'POST':
        form = FoodVendorForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('vendor_list')
    else:
        form = FoodVendorForm()
    return render(request, 'vendor/add_vendor.html', {"form": form})
