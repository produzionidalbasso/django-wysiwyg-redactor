from django import forms
from django.core import signing
from django.core.signing import BadSignature


class ImageForm(forms.Form):
    file = forms.ImageField()


class FileForm(forms.Form):
    file = forms.FileField()


class ActionTokenValidationForm(forms.Form):

    token = forms.CharField(required=True)

    def get_id_from_token(self, session_id):
        payload = self.cleaned_data["token"]

        signer = signing.Signer(salt=session_id)

        try:
            return signer.unsign(payload)
        except BadSignature:
            return False
