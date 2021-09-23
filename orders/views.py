from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from carts.models import Cart, CartItem
from .forms import OrderForm
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse

from .models import Order, Payment, Order_Product
from store.models import Product
import datetime
import json

# Create your views here.
@login_required(login_url = 'login')
def place_order(request):
    
    current_user = request.user
    
    # if cart item count is less than or equal to 0, return to store
    cart_items = CartItem.objects.filter(user=current_user)
    cart_item_count = cart_items.count()

    if cart_item_count <= 0:
        return redirect('store')

    total =0
    quantity =0
       
    for cart_item in cart_items:
        total += (cart_item.product_id.price * cart_item.quantity)
        quantity += cart_item.quantity

    tax = round((.02 * total),2)
    grand_total = total + tax

    if request.method == "POST":
        order_form = OrderForm(request.POST)

        if order_form.is_valid():
            order = Order()
            order.first_name = order_form.cleaned_data['first_name']
            order.last_name = order_form.cleaned_data['last_name']
            order.phone = order_form.cleaned_data['phone']
            order.email = order_form.cleaned_data['email']
            order.address_line_1 = order_form.cleaned_data['address_line_1']
            order.address_line_2 = order_form.cleaned_data['address_line_2']
            order.country = order_form.cleaned_data['country']
            order.state = order_form.cleaned_data['state']
            order.city = order_form.cleaned_data['city']
            order.order_note = order_form.cleaned_data['order_note']
            order.user = current_user
            order.payment = None
            order.total = grand_total
            order.tax = tax
            order.ip = request.META.get("REMOTE_ADDR")

            order.save()

            # Generate order number
            yr = int(datetime.date.today().strftime("%Y"))
            mt = int(datetime.date.today().strftime("%m"))
            dy = int(datetime.date.today().strftime("%d"))
            date = datetime.date(yr,mt,dy)
            id = date.strftime("%Y%m%d") + str(order.id)
            order.order_number = id
            order.save()

            order = Order.objects.get(user=current_user, is_ordered=False, order_number =id)
            context = {
                'total': total,
                'order': order,
                'cart_items' : cart_items,
                'tax': tax,
                'grand_total': grand_total
            }
            return render(request, 'order/payment.html', context)
        
        else:
            return redirect('checkout')

    else:
        return redirect('checkout')

def payments(request):

    body = json.loads(request.body)
    current_user = request.user

    order = Order.objects.get(user= current_user, is_ordered=False, order_number=body['orderID'])
    payment = Payment(
        user= current_user,
        payment_id= body['tranID'],
        payment_method= body['payment_method'],
        status= body['status'],
        amount_paid=body['amount_paid']
    )

    payment.save()

    order.payment = payment
    order.is_ordered = True
    order.save()

    # Move cart items to product order
    cart_items = CartItem.objects.filter(user=current_user)

    for cart_item in cart_items:
        order_product = Order_Product()
        order_product.order_id = order.id
        order_product.payment = payment
        order_product.user_id = request.user.id 
        order_product.product_id = cart_item.product_id.id
        order_product.quantity = cart_item.quantity
        order_product.product_price = cart_item.product_id.price
        order_product.is_ordered = True

        order_product.save()
        
        item = CartItem.objects.get(id=cart_item.id)
        product_variation = item.variation.all()
        order_product = Order_Product.objects.get(id = order_product.id)
        order_product.variation.set(product_variation)
        order_product.save()

        # Decrease quantity of product when it is orders
        product = Product.objects.get(id = cart_item.product_id_id)
        product.stock -= cart_item.quantity
        product.save()

    # clear cart
    CartItem.objects.filter(user=current_user).delete()

    # send email to customer
    mail_subject = 'Thank You for ordering'

    message = render_to_string('order/order_reccieved_email.html',
                { 'user': current_user,
                'order': order
                }) 
    to_email = request.user.email
    send_email = EmailMessage(mail_subject, message, to=[to_email])
    send_email.send()

    #send order no and transition id to user
    data ={
        'order_no': order.order_number,
        'tranID': payment.payment_id,
    }

    return JsonResponse(data)

def order_complete(request):
    order_no = request.GET.get('order_number')
    tranID = request.GET.get('payment_id')

    try:
        order = Order.objects.get(order_number=order_no, is_ordered=True)
        ordered_product = Order_Product.objects.filter(order_id = order.id)
        payment = Payment.objects.get(payment_id=tranID)

        subtotal = 0

        for item in ordered_product:
            subtotal += (item.quantity * item.product_price)

        context = {
            'order':order,
            'ordered_product':ordered_product,
            'order_no':order.order_number,
            'tranID':payment.payment_id,
            'payment':payment,
            'subtotal' : subtotal,       
        }
        return render(request, 'order/order_complete.html',context)

    except (Order.DoesNotExist, Order_Product.DoesNotExist):
        return redirect('home')
