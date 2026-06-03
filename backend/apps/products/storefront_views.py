from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.cart.models import Cart, CartItem
from apps.orders.models import Order, OrderItem
from apps.products.models import Product


def catalog_page(request):
    products = Product.objects.select_related('category').order_by('title')
    return render(request, 'storefront/catalog.html', {'products': products})


def product_detail_page(request, product_id):
    product = get_object_or_404(Product.objects.select_related('category'), id=product_id)
    return render(request, 'storefront/product_detail.html', {'product': product})


def signup_page(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Аккаунт создан. Теперь можно оформлять заказ.')
            return redirect('storefront_catalog')
    else:
        form = UserCreationForm()

    return render(request, 'registration/signup.html', {'form': form})


@login_required
def cart_page(request):
    cart = get_user_cart(request.user)
    return render(request, 'storefront/cart.html', build_cart_context(cart))


@login_required
@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart = get_user_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        item.quantity += 1
        item.save(update_fields=['quantity'])

    messages.success(request, f'{product.title} добавлен в корзину.')
    return redirect(request.POST.get('next') or 'storefront_cart')


@login_required
@require_POST
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    quantity = int(request.POST.get('quantity') or 1)

    if quantity <= 0:
        item.delete()
        messages.info(request, 'Товар удалён из корзины.')
    else:
        item.quantity = quantity
        item.save(update_fields=['quantity'])
        messages.success(request, 'Количество обновлено.')

    return redirect('storefront_cart')


@login_required
@require_POST
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.info(request, 'Товар удалён из корзины.')
    return redirect('storefront_cart')


@login_required
def checkout_page(request):
    cart = get_user_cart(request.user)
    context = build_cart_context(cart)

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone_digits = ''.join(symbol for symbol in request.POST.get('phone_number', '') if symbol.isdigit())

        if not context['items']:
            messages.error(request, 'Корзина пустая. Добавьте товар перед оформлением заказа.')
            return redirect('storefront_cart')

        if not full_name or not phone_digits:
            messages.error(request, 'Укажите имя клиента и номер телефона.')
            return render(request, 'storefront/checkout.html', context)

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                full_name=full_name,
                email=request.user.email or 'client@example.com',
                phone_number=phone_digits,
                address='Не указан',
                total_price=context['total'],
                status='created',
            )

            for line in context['items']:
                for _ in range(line['item'].quantity):
                    OrderItem.objects.create(
                        order=order,
                        product=line['item'].product,
                        product_name=line['item'].product.title,
                        price=line['item'].product.price,
                    )

            cart.items.all().delete()

        messages.success(request, f'Заказ №{order.id} создан и сохранён в базе данных.')
        return redirect('storefront_catalog')

    return render(request, 'storefront/checkout.html', context)


def get_user_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def build_cart_context(cart):
    items = []
    total = Decimal('0')

    for item in cart.items.select_related('product', 'product__category'):
        subtotal = item.product.price * item.quantity
        items.append({'item': item, 'subtotal': subtotal})
        total += subtotal

    return {'cart': cart, 'items': items, 'total': total}
