from secrets import choice
from unittest.util import _MAX_LENGTH
from django.db import models
from user.models import User

import payments


payment_gateway_choices = (
    ("boku", "Boku"),
)

class Operator(models.Model):
    """
    Model to store the operator details
    """
    name = models.CharField(max_length=95)
    code = models.CharField(max_length=95)
    country = models.CharField(max_length=65)
    country_id = models.CharField(max_length=5)
    max_transaction_limit = models.FloatField()
    currency = models.CharField(max_length=65, default="euro")

    def __str__(self):
        return self.name + " " + self.country


class Msdin(models.Model):
    """
    Model to store the supported msdin for the country
    """
    operator = models.ForeignKey(Operator, on_delete=models.CASCADE, related_name="msdins")
    pattern = models.CharField(max_length=55)


class PrivateKey(models.Model):
    """
    Model for parent API Keys
    """
    payment_gateway = models.CharField(max_length=65, choices=payment_gateway_choices)
    key_text = models.TextField()
    modified_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.payment_gateway + "(Private)"


class PublicKey(models.Model):
    """
    Model for public api keys
    """
    payment_gateway = models.CharField(max_length=65, choices=payment_gateway_choices)
    key_text = models.TextField()
    modified_on = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.payment_gateway + "(Public)"


class BokuPayment(models.Model):
    """
    Model to store the status of payments made via BOKU.
    """

    charging_token = models.CharField(max_length=65, blank=True)
    authorisation_state = models.CharField(max_length=20, blank=True)
    operation_reference = models.CharField(unique=True, max_length=65)
    consumer_identity = models.CharField(max_length=65, blank=True)
    latest_update = models.DateTimeField(blank=True, null=True)
    billing_identity = models.CharField(max_length=25, blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return self.operation_reference


class BokuPaymentError(models.Model):
    """
    Model to store the errors if faces in a payment
    """

    payment = models.ForeignKey(BokuPayment, on_delete=models.CASCADE, related_name="errors")
    message = models.CharField(max_length=155)


class Charge(models.Model):
    """
    Model to store the payments charged
    """
    payment = models.ForeignKey(BokuPayment, on_delete=models.SET_NULL, null=True, related_name="charges")
    operation_reference = models.CharField(max_length=155)
    transaction_id = models.CharField(max_length=155)
    transaction_state = models.CharField(max_length=65)
    latest_update = models.DateTimeField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.transaction_id + " (%s)" % self.transaction_state


class ChargeError(models.Model):
    """
    Model to store the errors if faces in a payment
    """

    charge = models.ForeignKey(Charge, on_delete=models.CASCADE, related_name="errors")
    message = models.CharField(max_length=155)


class Refund(models.Model):
    """
    Model to store the refund processed
    """
    payment = models.ForeignKey(BokuPayment, on_delete=models.SET_NULL, null=True, related_name="refunds")
    operation_reference = models.CharField(max_length=155)
    refund_reason = models.TextField(blank=True)
    refund_status = models.CharField(max_length=155, blank=True)
    amount = models.FloatField(blank=True, null=True)
    transaction_id = models.CharField(max_length=155)
    latest_update = models.DateTimeField(blank=True, null=True)


class RefundError(models.Model):
    """
    Model to store the errors if faces in a refund
    """

    refund = models.ForeignKey(Refund, on_delete=models.CASCADE, related_name="errors")
    message = models.CharField(max_length=155)
