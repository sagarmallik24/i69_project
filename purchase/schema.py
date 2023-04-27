import graphene
from graphene import *
from user.models import User
from .models import Purchase, Package, PackagePurchase
from datetime import datetime


class purchaseResponseObj(graphene.ObjectType):
    id = graphene.Int()
    coins = graphene.Int()
    success = graphene.Boolean()


class purchaseCoin(graphene.Mutation):
    class Arguments:
        id = graphene.String()
        method = graphene.String()
        coins = graphene.Int()
        money = graphene.Float()
        payment_method = graphene.String()

    Output = purchaseResponseObj

    def mutate(self, info, id, coins, money, method="COINS",payment_method=None):
        user = User.objects.get(id=id)
        new_purchase = Purchase.objects.create(user=user, method=method, coins=coins, money=money,payment_method=payment_method)
        new_purchase.save()

        return purchaseResponseObj(id=new_purchase.purchase_id, coins=user.coins, success=True)


class purchasePackageObject(graphene.ObjectType):
    id = graphene.Int()
    success = graphene.Boolean()


class purchasePackageMutation(graphene.Mutation):
    class Arguments:
        package_id = graphene.Int()

    Output = purchasePackageObject

    def mutate(self, info, package_id):
        user = info.context.user
        package = Package.objects.get(id=package_id)
        purchase_package = PackagePurchase.objects.create(user=user, package=package, is_active=True)

        return purchasePackageObject(id=purchase_package.id, success=True)


class Query(graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    purchaseCoin = purchaseCoin.Field()
    purchasePackage = purchasePackageMutation.Field()



