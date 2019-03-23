from django import forms
from django.forms import fields,widgets
from repository.models import *
from django.core.exceptions import ValidationError

class TroubleMaker(forms.Form):
    title = fields.CharField(
        max_length=32,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
    )
    detail = fields.CharField(
        widget=widgets.Textarea(attrs={'id':'detail','class':'kind-content'}),
    )


class TroubleKill(forms.Form):
    title = fields.CharField(
        max_length=32,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        disabled=True,
        required=False,
    )
    solution = fields.CharField(
        widget=widgets.Textarea(attrs={'id':'solution','class':'kind-content'}),
    )