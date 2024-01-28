from django.shortcuts import render, get_list_or_404
from .models import *

def accept_order(request, deliverer_id, order_id):
    deliverer = get_list_or_404(Deliverer, pk=deliverer_id)
    order = get_list_or_404(Order, pk=order_id)

    # Check if there is an existing assignment for this order
    assignment, created = OrderAssignment.objects.get_or_create(deliverer=deliverer, order=order)

    assignment.accept_order()

    return render(request, ' ', {'deliverer': deliverer, 'order': order, 'assignment': assignment})