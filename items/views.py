from django.shortcuts import render, get_object_or_404, redirect
from .models import Gift, Wishlist, Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.db.models import Q

def get_gift_metadata(gift):
    name = gift.name.lower()
    meta = {
        "rating": "4.8",
        "rating_stars": range(5),
        "rating_count": 24,
        "image": "images/giftbox.jpg",
        "category": "Anniversary",
        "badge": "Featured",
        "is_new": False,
        "is_best": False,
        "is_personalized": False
    }
    
    if "frame" in name:
        meta["rating"] = "4.8"
        meta["rating_stars"] = range(5)
        meta["rating_count"] = 42
        meta["image"] = "images/frame.jpg"
        meta["category"] = "Personalized"
        meta["is_personalized"] = True
        meta["is_new"] = True
        meta["badge"] = "New"
    elif "giftbox" in name:
        meta["rating"] = "5.0"
        meta["rating_stars"] = range(5)
        meta["rating_count"] = 108
        meta["image"] = "images/giftbox.jpg"
        meta["category"] = "Anniversary"
        meta["is_best"] = True
        meta["badge"] = "Bestseller"
    elif "polaroid" in name:
        meta["rating"] = "4.7"
        meta["rating_stars"] = range(4)
        meta["rating_count"] = 67
        meta["image"] = "images/polaroid.jpg"
        meta["category"] = "Personalized"
        meta["is_personalized"] = True
        meta["is_new"] = True
        meta["badge"] = "New"
    elif "calender" in name or "calendar" in name:
        meta["rating"] = "4.9"
        meta["rating_stars"] = range(5)
        meta["rating_count"] = 55
        meta["image"] = "images/calendar.jpg"
        meta["category"] = "Birthday"
        meta["is_best"] = True
        meta["badge"] = "Popular"
    elif "rose" in name:
        meta["rating"] = "4.9"
        meta["rating_stars"] = range(5)
        meta["rating_count"] = 89
        meta["image"] = "images/rose_bouquet.jpg"
        meta["category"] = "Wedding"
        meta["is_best"] = True
        meta["badge"] = "Bestseller"
    elif "chocolate" in name:
        meta["rating"] = "4.8"
        meta["rating_stars"] = range(5)
        meta["rating_count"] = 34
        meta["image"] = "images/chocolates_bouquet.jpg"
        meta["category"] = "Festival"
        meta["is_new"] = True
        meta["badge"] = "Featured"
        
    return meta

def home(request):
    search = request.GET.get("search")
    gifts = Gift.objects.all()

    if search:
        gifts = gifts.filter(
            Q(name__icontains=search) |
            Q(details__icontains=search)
        )

    for gift in gifts:
        meta = get_gift_metadata(gift)
        for key, val in meta.items():
            setattr(gift, key, val)

    return render(request, "items/home.html", {
        "gifts": gifts,
        "cart_count": Cart.objects.count(),
        "wishlist_count": Wishlist.objects.count(),
    })

def gift_detail(request, id):
    gift = get_object_or_404(Gift, id=id)
    meta = get_gift_metadata(gift)
    for key, val in meta.items():
        setattr(gift, key, val)

    return render(request, "items/details.html", {
        "gift": gift,
        "cart_count": Cart.objects.count(),
        "wishlist_count": Wishlist.objects.count(),
    })

@login_required
def add_to_wishlist(request, id):
    gift = get_object_or_404(Gift, id=id)

    if Wishlist.objects.filter(gift=gift).exists():
        messages.warning(request, "Product is already in your Wishlist!")
    else:
        Wishlist.objects.create(gift=gift)
        messages.success(request, "Product added to Wishlist successfully!")

    return redirect('home')

@login_required
def wishlist(request):
    gifts = Wishlist.objects.all()
    for item in gifts:
        meta = get_gift_metadata(item.gift)
        for key, val in meta.items():
            setattr(item.gift, key, val)

    return render(request, "items/wishlist.html", {
        "gifts": gifts,
        "cart_count": Cart.objects.count(),
        "wishlist_count": Wishlist.objects.count(),
    })

@login_required
def add_to_cart(request, id):
    gift = get_object_or_404(Gift, id=id)
    cart_item = Cart.objects.filter(gift=gift).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(gift=gift, quantity=1)

    messages.success(request, "Product added to Cart successfully!")
    return redirect('/')

@login_required
def cart(request):
    cart_items = Cart.objects.all()
    total = 0

    for item in cart_items:
        total += item.gift.price * item.quantity
        meta = get_gift_metadata(item.gift)
        for key, val in meta.items():
            setattr(item.gift, key, val)

    return render(request, "items/cart.html", {
        "cart_items": cart_items,
        "total": total,
        "cart_count": Cart.objects.count(),
        "wishlist_count": Wishlist.objects.count(),
    })

@login_required
def increase_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

@login_required
def decrease_quantity(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

@login_required
def delete_cart_item(request, id):
    cart_item = get_object_or_404(Cart, id=id)
    cart_item.delete()
    return redirect('cart')

@login_required
def delete_wishlist(request, id):
    item = get_object_or_404(Wishlist, id=id)
    item.delete()
    messages.success(request, "Product removed from Wishlist.")
    return redirect('wishlist')

@login_required
def move_to_cart(request, id):
    item = get_object_or_404(Wishlist, id=id)
    cart_item = Cart.objects.filter(gift=item.gift).first()

    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        Cart.objects.create(gift=item.gift, quantity=1)

    item.delete()
    messages.success(request, "Product moved to Cart.")
    return redirect('wishlist')

def about(request):
    cart_count = Cart.objects.count()
    wishlist_count = Wishlist.objects.count()
    return render(request, "items/about.html", {
        "cart_count": cart_count,
        "wishlist_count": wishlist_count,
    })

def contact(request):
    if request.method == "POST":
        messages.success(request, "Thank you for reaching out! Our design concierge team will reply via email or phone shortly.")
        return redirect('contact')
    
    cart_count = Cart.objects.count()
    wishlist_count = Wishlist.objects.count()
    return render(request, "items/contact.html", {
        "cart_count": cart_count,
        "wishlist_count": wishlist_count,
    })

def faq_returns(request):
    cart_count = Cart.objects.count()
    wishlist_count = Wishlist.objects.count()
    return render(request, "items/faq_returns.html", {
        "cart_count": cart_count,
        "wishlist_count": wishlist_count,
    })
