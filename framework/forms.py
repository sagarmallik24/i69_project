from django.contrib.auth.forms import PasswordChangeForm
from django.forms import Select, TextInput, CharField
from django_otp.forms import OTPAuthenticationFormMixin


class CustomPasswordChangeForm(OTPAuthenticationFormMixin, PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(OTPAuthenticationFormMixin, self).__init__(*args, **kwargs)

    otp_device = CharField(required=False, widget=Select)
    otp_token = CharField(required=False, widget=TextInput(attrs={"autocomplete": "off"}))
    otp_challenge = CharField(required=False)

    def get_user(self):
        err = self.errors.as_data().get("__all__", None)
        print(err)
        return self.request.user if self.request.user and self.request.method == "POST" else None

    def clean(self):
        self.cleaned_data = super().clean()
        self.clean_otp(self.get_user())
        return self.cleaned_data
