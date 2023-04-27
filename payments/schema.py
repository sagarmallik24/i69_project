import graphene
from graphene import *
from graphene_django import DjangoObjectType

from geopy.geocoders import Nominatim

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import get_object_or_404

from user.models import User

from payments import models
from payments.boku import Boku


class BokuPaymentType(DjangoObjectType):
    class Meta:
        model = models.BokuPayment
        fields = ('id', 'charging_token', 'authorisation_state',
                  'billing_identity', 'operation_reference')


class availableBokuOperatorsResponse(graphene.ObjectType):
    operators = graphene.List(graphene.String)


class availableBokuOperators(graphene.Mutation):
    class Arguments:
        latitude = graphene.String()
        longitude = graphene.String()

    Output = availableBokuOperatorsResponse

    def mutate(self, info, latitude, longitude):
        geolocator = Nominatim(user_agent="framework")
        location = geolocator.reverse("%s, %s" % (latitude, longitude), exactly_one=True)
        country = location.address.split(",")[-1].strip()

        operators_list = list(
            models.Operator.objects\
                .filter(country=country)\
                .values_list('code', flat=True)
            )

        return availableBokuOperatorsResponse(operators=operators_list)


class mobilePinInputResponse(graphene.ObjectType):
    operation_reference = graphene.String()
    id = graphene.Int()
    success = graphene.Boolean()


class mobilePinInput(graphene.Mutation):
    class Arguments:
        code = graphene.Int()
        charging_token = graphene.String()

    Output = mobilePinInputResponse

    def mutate(self, info, code, charging_token):
        boku_payment = get_object_or_404(models.BokuPayment, charging_token=charging_token)
        boku = Boku()
        callback = info.context.headers['Origin'] + "/payments/webhook/boku/authorisation/"
        #callback = "https://6bf9-2405-201-6806-911d-f0c9-f699-f20c-3f02.in.ngrok.io" + "/payments/webhook/boku/authorisation/"
        body = {
            "flow": {
                "pin": {
                    "channel_code": "sandbox-ee",
                    "msisdn": boku_payment.billing_identity,
                    "code": str(code)
                }
            },
            "country": "EE",
            "merchant": "162350b61495c7d69dcc6a63973ae75f",
            "operation_reference": boku_payment.operation_reference,
            "callback": callback,
        }

        url = "https://api-jwt.fortumo.io/authorisations/" + str(charging_token)

        response = boku.make_put_request(url, body=body)

        if response:
            return mobilePinInputResponse(
                operation_reference=boku_payment.operation_reference,
                id=id,
                success=True
            )
        else:
            return mobilePinInputResponse(
                operation_reference="",
                id=0,
                success=False
            )


class chargePaymentResponse(graphene.ObjectType):
    charging_token = graphene.String()
    id = graphene.Int()
    success = graphene.Boolean()


class refundPaymentResponse(graphene.ObjectType):
    payment_reference = graphene.String()
    id = graphene.Int()
    success = graphene.Boolean()


class refundPayment(graphene.Mutation):
    class Arguments:
        payment_reference = graphene.String()
        refund_reason = graphene.String()
        amount = graphene.Float()

    Output = refundPaymentResponse

    def mutate(self, info, payment_reference, amount, refund_reason):
        charge = get_object_or_404(
            models.Charge,
            operation_reference=payment_reference
        )

        boku = Boku()

        callback = info.context.headers['Origin'] + "/payments/webhook/boku/refund/"
        #callback = "https://6bf9-2405-201-6806-911d-f0c9-f699-f20c-3f02.in.ngrok.io" + "/payments/webhook/boku/refund/"

        body = {
            "payment_operation_reference": payment_reference,
            "refund_reason": refund_reason,
            "merchant": "377b7cdc1716225e7766a7a46e0bbb73",
            "operation_reference": "refund_" + str(charge.payment.id),
            "callback": callback,
            "amount": {
                "value": amount,
                "currency": "EUR"
            }
        }

        url = "https://api-jwt.fortumo.io/refunds"

        response = boku.make_post_request(url, body=body)

        if response:
            return refundPaymentResponse(
                payment_reference=payment_reference,
                success=True
            )
        else:
            return refundPaymentResponse(
                payment_reference=payment_reference,
                success=False
            )


class chargePayment(graphene.Mutation):
    class Arguments:
        charging_token = graphene.String()
        amount = graphene.Float()
        description = graphene.String()

    Output = chargePaymentResponse

    def mutate(self, info, charging_token, amount, description):
        boku_payment = get_object_or_404(
            models.BokuPayment,
            charging_token=charging_token
        )

        boku = Boku()

        callback = info.context.headers['Origin'] + "/payments/webhook/boku/charge/"
        #callback = "https://6bf9-2405-201-6806-911d-f0c9-f699-f20c-3f02.in.ngrok.io" + "/payments/webhook/boku/charge/"

        body = {
            "item_description": description,
            "amount": {
                "value": str(amount),
                "currency": "EUR"
            },
            "charging_token": charging_token,
            "merchant": "162350b61495c7d69dcc6a63973ae75f",
            "operation_reference": "charge-payment" + str(boku_payment.id),
            "callback": callback
        }

        url = "https://api-jwt.fortumo.io/payments"

        response = boku.make_post_request(url, body=body)

        if response:
            return chargePaymentResponse(
                charging_token=boku_payment.charging_token,
                success=True
            )
        else:
            return mobilePinInputResponse(
                charging_token=boku_payment.charging_token,
                success=False
            )


class pinAuthorisationResponse(graphene.ObjectType):
    operation_reference = graphene.String()
    id = graphene.Int()
    user_id = graphene.Int()
    success = graphene.Boolean()


class pinAuthorisation(graphene.Mutation):
    class Arguments:
        user_id = graphene.String()
        mobile_number = graphene.String()
        recurring_payment = graphene.Boolean()
        operator_code = graphene.String()

    Output = pinAuthorisationResponse

    def mutate(self, info, mobile_number, recurring_payment, user_id, operator_code):
        user = User.objects.get(id=user_id)
        boku_payment = models.BokuPayment(operation_reference="initial")
        boku = Boku()

        boku_payment.save()

        id = boku_payment.id

        operation_reference = "payment" + str(id)

        boku_payment.operation_reference = operation_reference
        boku_payment.user = user
        payment_type = "onetime"

        if recurring_payment:
            payment_type = "subscription"

        callback = info.context.headers['Origin'] + "/payments/webhook/boku/authorisation/"
        #callback = "https://6bf9-2405-201-6806-911d-f0c9-f699-f20c-3f02.in.ngrok.io" + "/payments/webhook/boku/authorisation/"
        body = {
            "flow": {
                "pin": {
                    "channel_code": operator_code,
                    "msisdn": mobile_number,
                    "code": ""
                }
            },
            "country": "EE",
            "merchant": "162350b61495c7d69dcc6a63973ae75f",
            "operation_reference": operation_reference,
            "callback": callback,
            "payment_type": payment_type
        }

        boku_payment.billing_identity = mobile_number

        response = boku.make_post_request("https://api-jwt.fortumo.io/authorisations", body=body)

        if response:
            boku_payment.save()
            return pinAuthorisationResponse(operation_reference=operation_reference, id=id, success=True)
        else:
            boku_payment.delete()
            return pinAuthorisationResponse(operation_reference="", id=0, success=False)


class Query(graphene.ObjectType):
    payment_by_operation_reference = graphene.Field(
        BokuPaymentType,
        operation_reference=graphene.String(
            required=True
        )
    )

    def resolve_payment_by_operation_reference(root, info, operation_reference):
        try:
            return models.BokuPayment.objects\
                .get(operation_reference=operation_reference)
        except models.BokuPayment.DoesNotExist:
            return None


class Mutation(graphene.ObjectType):
    pinAuthorisation = pinAuthorisation.Field()
    mobilePinInput = mobilePinInput.Field()
    chargePayment = chargePayment.Field()
    refundPayment = refundPayment.Field()
    availableBokuOperators = availableBokuOperators.Field()