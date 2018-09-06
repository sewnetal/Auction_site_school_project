from django import forms
from YAAS.models import Auction
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class Auction_form(forms.Form):
    title =forms.CharField()
    description = forms.CharField(widget=forms.Textarea())
    min_price = forms.FloatField()
    category = forms.CharField()
    end_date = forms.DateTimeField(input_formats=['%Y-%m-%d %H:%M'], help_text="(Year-Month-Day Hour:Min)")
class Confirm_auction(forms.Form):
    CHOICES = [(x,x) for x in ("Yes","No")]
    option = forms.ChoiceField(choices=CHOICES)
    a_title = forms.CharField(widget=forms.HiddenInput)
class Registration_form(UserCreationForm):
    firstname = forms.CharField(max_length=40)
    lastname = forms.CharField(max_length=40)
    email = forms.EmailField(required=True)
    CHOICES = [(x,x) for x in ("English","Finish")]
    language = forms.ChoiceField(choices=CHOICES)
    class Meta:
        model = User
        fields = ('firstname','lastname','email','password1','password2','language')
class Placebid(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ('min_price',)
class searchauction(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ('title',)
class Edit_description(forms.ModelForm):

    class Meta:
        model = Auction
        fields = ('description', )

