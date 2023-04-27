from django.db import models
from user.models import User
from django.db.models import F

from email.policy import default
from django.core.exceptions import ValidationError
from .utils import payment_method_choices

class Purchase(models.Model):
    purchase_id = models.BigAutoField(primary_key=True,unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    method = models.CharField(max_length=255)
    coins = models.IntegerField()
    money = models.DecimalField(max_digits = 5,decimal_places = 2)
    purchased_on = models.DateTimeField(auto_now_add=True, null=True)
    payment_method = models.CharField(max_length=255,default=None, null=True,blank=True) # choices = payment_method_choices,

    class Meta:
        verbose_name_plural = "Purchase"
        verbose_name = "Purchase"


    def __str__(self):
        return f"id:{self.purchase_id} {self.coins} coins by {self.user} on {self.purchased_on}"


    def save(self, *args, **kwargs):
        obj = super().save(*args, **kwargs)

        # Add Coins to user wallet.
        user = self.user
        user.purchase_coins = user.purchase_coins + self.coins
        user.purchase_coins_date = self.purchased_on
        user.save()

        return obj

class Package(models.Model):
    """
    Model for the packages available for purchase
    """
    name = models.CharField(max_length=65)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.name


class PackagePurchase(models.Model):
    """
    Model for packages that user purchase.
    """
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name="purchases")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="packages")
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.package) + " Package for user: " + str(self.user)

    def clean(self):
        user = self.user

        already_purchased = False

        if self.is_active:
            already_purchased = PackagePurchase.objects.filter(user=user, is_active=True).exists()

        if already_purchased:
            raise ValidationError("Active package already found for this user.")

