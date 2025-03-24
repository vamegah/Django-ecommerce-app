from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartItem
from store.models import Product, Variation

# Utility function to get the cart ID
def _cart_id(request):
    if not (cart := request.session.session_key):
        cart = request.session.create()
    return cart

# Remove a single quantity of an item from the cart
def remove_from_cart(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('carts')

# Remove an entire cart item
def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(product=product, cart=cart, id=cart_item_id).delete()
    return redirect('carts')

# Add a product to the cart
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product_variation = _get_product_variations(request, product)
    current_user = request.user

    if current_user.is_authenticated:
        cart_item = _handle_authenticated_user_cart(current_user, product, product_variation)
    else:
        cart = _get_or_create_cart(request)
        cart_item = _handle_guest_user_cart(cart, product, product_variation)

    cart_item.save()
    return redirect('cart')

# Display the cart
def carts(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        total, quantity = _calculate_cart_totals(cart_items)
        tax = 0.1 * total
        grand_total = total + tax
    except Cart.DoesNotExist:
        tax = grand_total = 0

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/carts.html', context)

# Helper functions
def _get_product_variations(request, product):
    product_variation = []
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variation.append(variation)
            except Variation.DoesNotExist:
                pass
    return product_variation

def _get_or_create_cart(request):
    cart, created = Cart.objects.get_or_create(cart_id=_cart_id(request))
    return cart

def _handle_authenticated_user_cart(user, product, product_variation):
    cart_item, created = CartItem.objects.get_or_create(product=product, user=user)
    if not created:
        _update_cart_item_variations(cart_item, product_variation)
    else:
        cart_item.quantity = 1
        cart_item.variations.set(product_variation)
    return cart_item

def _handle_guest_user_cart(cart, product, product_variation):
    cart_item, created = CartItem.objects.get_or_create(product=product, cart=cart)
    if not created:
        _update_cart_item_variations(cart_item, product_variation)
    else:
        cart_item.quantity = 1
        cart_item.variations.set(product_variation)
    return cart_item

def _update_cart_item_variations(cart_item, product_variation):
    existing_variations = list(cart_item.variations.all())
    if product_variation in existing_variations:
        cart_item.quantity += 1
    else:
        cart_item.variations.set(product_variation)
        cart_item.quantity = 1

def _calculate_cart_totals(cart_items):
    total = sum(item.product.price * item.quantity for item in cart_items)
    quantity = sum(item.quantity for item in cart_items)
    return total, quantity
