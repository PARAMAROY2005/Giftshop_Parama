from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Address, Order, OrderItem
from .forms import AddressForm
from items.models import Cart, Wishlist
from django.contrib import messages

def cart(request):
    return redirect('/cart/')

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders/my_orders.html', {
        'orders': orders,
        'cart_count': Cart.objects.count(),
        'wishlist_count': Wishlist.objects.count(),
    })

@login_required
def checkout(request):
    cart_items = Cart.objects.all()
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty! Add products first.")
        return redirect('home')
        
    total = sum(item.gift.price * item.quantity for item in cart_items)

    if request.method == "POST":
        form = AddressForm(request.POST)
        if form.is_valid():
            request.session['shipping_address'] = form.cleaned_data
            return redirect("payment")
    else:
        form = AddressForm()

    return render(request, "orders/checkout.html", {
        "form": form,
        "total": total,
        "cart_count": Cart.objects.count(),
        "wishlist_count": Wishlist.objects.count(),
    })

@login_required
def payment(request):
    cart_items = Cart.objects.all()
    if not cart_items.exists():
        messages.warning(request, "Your cart is empty!")
        return redirect('home')
        
    total = sum(item.gift.price * item.quantity for item in cart_items)
    shipping_address = request.session.get('shipping_address')
    if not shipping_address:
        messages.error(request, "Please enter your delivery address first.")
        return redirect('checkout')

    if request.method == "POST":
        # Create order in database
        order = Order.objects.create(
            user=request.user,
            total_price=total,
            status="Placed"
        )
        
        # Create order items
        for item in cart_items:
            OrderItem.objects.create(
                order=order,
                gift=item.gift,
                quantity=item.quantity,
                price=item.gift.price
            )
            
        # Create Address associated with this order
        Address.objects.create(
            order=order,
            fullname=shipping_address.get('fullname'),
            phone=shipping_address.get('phone'),
            address=shipping_address.get('address'),
            city=shipping_address.get('city'),
            state=shipping_address.get('state'),
            pincode=shipping_address.get('pincode')
        )
        
        # Clear Cart
        Cart.objects.all().delete()
        
        # Save order ID in session and clear address
        request.session['last_order_id'] = order.id
        if 'shipping_address' in request.session:
            del request.session['shipping_address']
            
        messages.success(request, "Order placed successfully! Thank you for shopping with us.")
        return redirect("success")

    return render(request, "orders/payment.html", {
        "total": total,
        "cart_count": Cart.objects.count(),
        "wishlist_count": Wishlist.objects.count(),
    })

@login_required
def success(request):
    order_id = request.session.get('last_order_id')
    order = get_object_or_404(Order, id=order_id) if order_id else None
    
    # Calculate delivery date (3-5 days from now)
    import datetime
    delivery_date = datetime.date.today() + datetime.timedelta(days=4)

    return render(request, "orders/success.html", {
        "order": order,
        "delivery_date": delivery_date.strftime("%d %B %Y"),
        "cart_count": Cart.objects.count(),
        "wishlist_count": Wishlist.objects.count(),
    })