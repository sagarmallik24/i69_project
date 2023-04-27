from django.core.management.base import BaseCommand
from django.core.management import call_command

from user.models import UserLimit
from gifts.models import GiftPurchaseMessageText
from chat.models import DeletedMessageDate

class Command(BaseCommand):
    def handle(self, *args, **options):
        # generate default pickers and generate translations
        call_command('set_default_pickers')

        # generate userLimit for stories, moments and multi-story
        UserLimit.objects.create(
            action_name='Stories',
            limit_value=2
        )
        UserLimit.objects.create(
            action_name='Moments',
            limit_value=2
        )
        UserLimit.objects.create(
            action_name='MultiStoryLimit',
            limit_value=5
        )
        UserLimit.objects.create(
            action_name='FreeProfilePhotos',
            limit_value=3
        )

        # generate giftpurchasemessagetext
        GiftPurchaseMessageText.objects.create(
            text="{0} has offered you {1} gift value {2} coins"
        )

        DeletedMessageDate.objects.create(
            no_of_days=7
        )

