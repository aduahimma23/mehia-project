from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from .models import Item, CartItems, Reviews
from django.contrib import messages
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView,)
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .decorators import *
from django.db.models import Sum
from django.views import View
from .forms import CartItemForm


def menuDetail(request, slug):
    item = Item.objects.filter(slug=slug).first()
    reviews = Reviews.objects.filter(rslug=slug).order_by('-id')[:10] 
    context = {
        'item' : item,
        'reviews' : reviews,
    }
    return render(request, 'cart/dishes.html', context)

@login_required
def add_reviews(request):
    if request.method == "POST":
        user = request.user
        rslug = request.POST.get("rslug")
        item = Item.objects.get(slug=rslug)
        review = request.POST.get("review")

        reviews = Reviews(user=user, item=item, review=review, rslug=rslug)
        reviews.save()
        messages.success(request, "Thank You for Reviewing this Item!!")
    return redirect(f"/dishes/{item.slug}")


class ItemCreateView(LoginRequiredMixin, CreateView):
    model = Item
    fields = ['title', 'image', 'description', 'price', 'pieces', 'instructions', 'labels', 'label_colour', 'slug']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)
    
@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, item_creted = CartItems.objects.get_or_create(cart=cart, product=product)

    if not item_creted:
        cart_item.quantity +=1
        cart_item.save()

    return redirect('cart_view')

def remove_from_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItems, pk=cart_item_id)
    cart_item.delete()

    return redirect('cart_view')

@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = CartItems.objects.filter(cart=cart)

    total = sum(request, 'cart/cart.htm', {'cart_items': cart_items, 'total': total})

def update_cart(request, cart_item_id):
    cart_item = get_object_or_404(CartItems, pk=cart_item_id)

    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()

    return redirect('cart_item')


class OrderTrackingView(View):
    template_name =' order_tracking.html'

    def get(self, request, order_id):
        order_tracking = get_object_or_404(OrderTracking, order__id=order_id)
        return render(request, self.template_name, {'order_tracking': order_tracking})
    


