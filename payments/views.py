import json
import datetime
from time import time

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import payments.models as models


@csrf_exempt
def boku_refund_payment_callback(request):
    """
    Webhook to handle the callback from the boku's refund api
    """

    body = json.loads(request.body)

    refund, created = models.Refund.objects\
        .get_or_create(operation_reference=body['operation_reference'])

    boku_payment = models.BokuPayment.objects\
        .get(
            consumer_identity=body['consumer_identity'],
            authorisation_state="verified"
        )

    timestamp = datetime.datetime\
        .strptime(body['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

    refund.payment = boku_payment
    refund.refund_status = body['refund_status']
    refund.amount = body['refund_amount']['value']
    refund.transaction_id = body['transaction_id']
    refund.latest_update = timestamp

    refund.save()

    if body.get('error', None):
        error, created = models.RefundError.objects\
            .get_or_create(refund=refund)

        error.message = body['error']['message']
        error.save()

    response = JsonResponse({'success': True})
    return response


@csrf_exempt
def boku_charge_payment_callback(request):
    """
    Webhook to handle the callback from the boku's charge api
    """
    body = json.loads(request.body)

    charge, created = models.Charge.objects\
        .get_or_create(operation_reference=body['operation_reference'])

    boku_payment = models.BokuPayment.objects.get(consumer_identity=body['consumer_identity'], authorisation_state="verified")

    timestamp = datetime.datetime\
        .strptime(body['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

    charge.payment = boku_payment

    charge.transaction_id = body['transaction_id']
    charge.transaction_state = body['transaction_state']
    charge.price = body['price']['amount']
    charge.latest_update = timestamp

    charge.save()

    if body.get('error', None):
        error, created = models.ChargeError.objects\
            .get_or_create(charge=charge)

        error.message = body['error']['message']
        error.save()

    response = JsonResponse({'success': True})
    return response


@csrf_exempt
def boku_pin_authorisation_callback(request):
    """
    Webhook to handle the callback from the boku's pin authorization
    """

    body = json.loads(request.body)

    boku_payment = get_object_or_404(
        models.BokuPayment,
        operation_reference=body['operation_reference']
    )

    timestamp = datetime.datetime\
        .strptime(body['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ')

    boku_payment.charging_token = body['charging_token']
    boku_payment.authorisation_state = body['authorisation_state']
    boku_payment.latest_update = timestamp
    boku_payment.consumer_identity = body['consumer_identity']

    boku_payment.save()

    if body.get('error', None):
        error, created = models.BokuPaymentError.objects\
            .get_or_create(payment=boku_payment)

        error.message = body['error']['message']
        error.save()

    response = JsonResponse({'success': True})
    return response