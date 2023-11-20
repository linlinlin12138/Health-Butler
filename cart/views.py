from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from healthbutler.models import Foods
from .cart import Cart
from .forms import CartAddFoodForm
from django.contrib.auth.decorators import login_required

@login_required()
@require_POST
def cart_add(request, food_id):
    cart = Cart(request)
    food = get_object_or_404(Foods, id=food_id)
    form = CartAddFoodForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(food=food,serving=cd['serving'])
    return redirect('cart:cart_detail')

@login_required()
def cart_remove(request, food_id):
    cart = Cart(request)
    food = get_object_or_404(Foods, id=food_id)
    cart.remove(food)
    return redirect('cart:cart_detail')


@login_required()
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'details.html', {'cart': cart})
