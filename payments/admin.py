from django.contrib import admin
from payments import models

admin.site.register(models.BokuPayment)
admin.site.register(models.BokuPaymentError)
admin.site.register(models.PrivateKey)
admin.site.register(models.PublicKey)
admin.site.register(models.Charge)
admin.site.register(models.ChargeError)
admin.site.register(models.Refund)
admin.site.register(models.RefundError)
admin.site.register(models.Operator)