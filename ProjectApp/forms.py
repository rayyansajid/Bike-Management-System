from django import forms

class PackageEditForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput)
    order_received_on = forms.DateField()
    status = forms.CharField()
    instructions = forms.CharField()
    city = forms.CharField()
    