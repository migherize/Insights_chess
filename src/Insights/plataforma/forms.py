from django import forms

class Login(forms.Form):
    username = forms.CharField(label='Usuario', max_length=30)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(), max_length=100)

class Register(forms.Form):
    username = forms.CharField(label='Usuario', max_length=30)
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput(), max_length=100)

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()