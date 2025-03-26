from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product, Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.db.models import F

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

# def add_to_cart(request, product_id):
#     current_user = request.user
#     product = get_object_or_404(Product, id=product_id)
#     product_variation = []

#     if request.method == 'POST':
#         for key, value in request.POST.items():
#             try:
#                 variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
#                 product_variation.append(variation)
#             except Variation.DoesNotExist:
#                 pass

#     if current_user.is_authenticated:
#         cart_item_query = CartItem.objects.filter(product=product, user=current_user)
#     else:
#         cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
#         cart_item_query = CartItem.objects.filter(product=product, cart=cart)

#     if cart_item_query.exists():
#         ex_var_list = []
#         id_list = []
#         for item in cart_item_query:
#             ex_var_list.append(list(item.variations.all()))
#             id_list.append(item.id)

#         if product_variation in ex_var_list:
#             index = ex_var_list.index(product_variation)
#             item_id = id_list[index]
#             cart_item = CartItem.objects.get(id=item_id)
#             cart_item.quantity += 1
#             cart_item.save()
#         else:
#             cart_item = cart_item_query.create(product=product, quantity=1, user=current_user if current_user.is_authenticated else None, cart=None if current_user.is_authenticated else cart)
#             if product_variation:
#                 cart_item.variations.set(product_variation)
#             cart_item.save()
#     else:
#         cart_item = CartItem.objects.create(
#             product=product,
#             quantity=1,
#             user=current_user if current_user.is_authenticated else None,
#             cart=None if current_user.is_authenticated else cart,
#         )
#         if product_variation:
#             cart_item.variations.set(product_variation)
#         cart_item.save()

#     return redirect('cart')

def add_to_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)  # Better error handling

    # Extract variations once for both authenticated and non-authenticated paths
    product_variation = []
    if request.method == 'POST':
        for key, value in request.POST.items():
            try:
                variation = Variation.objects.select_related('product').get(
                    product=product,
                    variation_category__iexact=key,
                    variation_value__iexact=value
                )
                product_variation.append(variation)
            except Variation.DoesNotExist:
                continue

    if current_user.is_authenticated:
        return handle_authenticated_cart(current_user, product, product_variation)
    else:
        return handle_anonymous_cart(request, product, product_variation)

def handle_authenticated_cart(user, product, product_variation):
    # Use get_or_create to reduce database queries
    cart_items = CartItem.objects.filter(product=product, user=user)
    
    if cart_items.exists():
        ex_var_list = []
        id_list = []
        # Use select_related to optimize database queries
        for item in cart_items.select_related('product'):
            existing_variation = list(item.variations.all())
            ex_var_list.append(existing_variation)
            id_list.append(item.id)

        if product_variation in ex_var_list:
            # Update quantity using F() expression to avoid race conditions
            index = ex_var_list.index(product_variation)
            CartItem.objects.filter(id=id_list[index]).update(
                quantity=F('quantity') + 1
            )
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=user
            )
            if product_variation:
                cart_item.variations.add(*product_variation)
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            user=user
        )
        if product_variation:
            cart_item.variations.add(*product_variation)
    
    return redirect('cart')

def handle_anonymous_cart(request, product, product_variation):
    cart, _ = Cart.objects.get_or_create(cart_id=_cart_id(request))
    
    cart_items = CartItem.objects.filter(product=product, cart=cart)
    
    if cart_items.exists():
        ex_var_list = []
        id_list = []
        for item in cart_items.select_related('product'):
            existing_variation = list(item.variations.all())
            ex_var_list.append(existing_variation)
            id_list.append(item.id)

        if product_variation in ex_var_list:
            index = ex_var_list.index(product_variation)
            CartItem.objects.filter(id=id_list[index]).update(
                quantity=F('quantity') + 1
            )
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                cart=cart
            )
            if product_variation:
                cart_item.variations.add(*product_variation)
    else:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart
        )
        if product_variation:
            cart_item.variations.add(*product_variation)
    
    return redirect('cart')



# def remove_from_cart(request, product_id, cart_item_id):

#     product = get_object_or_404(Product, id=product_id)
#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
#         else:
#             cart = Cart.objects.get(cart_id=_cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
#         if cart_item.quantity > 1:
#             cart_item.quantity -= 1
#             cart_item.save()
#         else:
#             cart_item.delete()
#     except:
#         pass
#     return redirect('cart')



def remove_from_cart(request, product_id, cart_item_id):
    """
    Remove or decrease quantity of an item from the cart.
    Args:
        request: HTTP request object
        product_id: ID of the product to remove
        cart_item_id: ID of the cart item
    Returns:
        Redirects to cart page
    """
    try:
        # Get product first to ensure it exists
        product = get_object_or_404(Product, id=product_id)
        
        # Build query based on authentication status
        cart_item_query = {
            'product': product,
            'id': cart_item_id
        }
        
        if request.user.is_authenticated:
            cart_item_query['user'] = request.user
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item_query['cart'] = cart

        # Get cart item with select_related to optimize query
        cart_item = CartItem.objects.select_related('product').get(**cart_item_query)

        if cart_item.quantity > 1:
            # Use F() expression for atomic update
            CartItem.objects.filter(id=cart_item_id).update(quantity=F('quantity') - 1)
        else:
            cart_item.delete()

    except ObjectDoesNotExist:
        # Log error if needed
        pass
    
    return redirect('cart')



def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
    else:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')


def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)

