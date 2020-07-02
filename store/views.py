from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart, cartData, guestOrder
from django.contrib import messages

# Create your views here.




def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.product_active.all()
    context = {'products': products, 'cartItems':cartItems}
    return render(request, 'store/store.html', context)

def product_single(request, pk):
    data = cartData(request)
    cartItems = data['cartItems']

    product = get_object_or_404(Product, pk=pk)
    context = {'product': product, 'cartItems':cartItems}
    return render(request, 'store/product_single.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']


    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'store/cart.html', context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all() # parent items
        '''NEW'''

        for item in items:
            if item.product.quantity < item.quantity:
                item.quantity = item.product.quantity
                messages.warning(request, f'В наличии только {item.product.quantity}  {item.product.name}')

        '''NEW'''

        cartItems = order.get_cart_items
    else:
        cookieData = cookieCart(request)
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']
        '''NEW'''
        for item in items:
            product_in_storage = Product.objects.get(id=item['product']['id'])
            if product_in_storage.quantity < item['quantity']:
                item['quantity'] = product_in_storage.quantity

                messages.warning(request, f'В наличии только {product_in_storage.quantity} {product_in_storage.name}')
        '''NEW'''



    context = {'items': items, 'order': order, 'cartItems':cartItems}
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action: ', action)
    print('productId: ', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity+1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity-1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()


    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)
    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
        )

    return JsonResponse('Payment complete', safe=False)

