from django import forms

class URLForm(forms.Form):

    url = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Directory Location'}))
