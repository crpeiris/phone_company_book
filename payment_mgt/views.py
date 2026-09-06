import logging

from django.shortcuts import render

import stripe
from django.conf import settings
from django.shortcuts import redirect
from django.http import JsonResponse
from store.models import Order
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


stripe.api_key = settings.STRIPE_SECRET_KEY


# Exempt CSRF for this view only since it's dealing with Stripe Checkout
from django.shortcuts import redirect


@csrf_exempt
def create_checkout_session(request, order_id):
    if request.method == "POST":
        try:
            order = Order.objects.get(id=order_id, customer=request.user)


            total_price = sum(
                item.product.sale_price * item.quantity
                for item in order.orderproduct_set.all()
            )


            session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'product_data': {
                                'name': 'Your Order',
                            },
                            'unit_amount': int(total_price * 100),  # Stripe accepts amounts in cents
                        },
                        'quantity': 1,
                    },
                ],
                metadata={
                    'user_id': request.user.id,
                    'order_id': order_id,
                },
                mode='payment',
                success_url='https://mistakenly-growing-kiwi.ngrok-free.app/payment_mgt/payment_success/',
                cancel_url='https://mistakenly-growing-kiwi.ngrok-free.app/payment_mgt/payment_decline/',
            )


            # Redirect to Stripe Checkout session URL
            return redirect(session.url)
        except Exception as e:
            logger = logging.getLogger(__name__)
            logger.error(f"Error creating checkout session: {e}")
            return JsonResponse({'error': str(e)}, status=500)

# Payment success view without csrf exemption
def payment_success(request):
    return render(request, 'payment_mgt/pay_success.html', {'message': 'Payment Success!'})


# Payment decline view without csrf exemption
def payment_decline(request):
    return render(request, 'payment_mgt/payment_decline.html', {'Title': 'Payment Decline!'})

# Webhook endpoint for Stripe payment success, CSRF exempted
@csrf_exempt
def payment_success_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)

    if not endpoint_secret:
        return JsonResponse({'error': 'STRIPE_WEBHOOK_SECRET missing in settings'}, status=500)

    if not sig_header:
        return JsonResponse({'error': 'Missing signature header'}, status=400)

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except (ValueError, stripe.error.SignatureVerificationError) as e:
        return JsonResponse({'error': f'Verification failed: {str(e)}'}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # Convert the Stripe Session object into a standard dictionary
        session_data = session.to_dict()
        metadata = session_data.get('metadata', {})
        order_id = metadata.get('order_id')

        if not order_id:
            return JsonResponse({'error': 'order_id not found in session metadata'}, status=400)

        try:
            payment_intent_id = session_data.get('payment_intent')
            process_order = Order.objects.get(id=order_id)
            
            process_order.pay_refrence = payment_intent_id
            process_order.status = "paid"
            process_order.save()
        except Order.DoesNotExist:
            return JsonResponse({'error': f'Order {order_id} not found'}, status=404)

    return JsonResponse({'status': 'success'}, status=200)