from typing import Any
from django import forms
from app_auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    terms = forms.BooleanField(required=True, label="Acepto los términos y condiciones")

    class Meta:
        model = User
        fields = ["email","first_name","last_name","phone_number"]

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        print("Cleaning email")
        if User.objects.filter(email__iexact=email).exists():
            print("Email exists")
            raise forms.ValidationError("Ya existe un usuario registrado con este correo electrónico")
        return email
    
    def clean_terms(self):
        terms = self.cleaned_data.get('terms')
        if not terms:
            print("Terms not accepted")
            raise forms.ValidationError("Debe aceptar los términos y condiciones para continuar.")
        return terms
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        print("Cleaning password")
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            print("Passwords do not match")
            raise forms.ValidationError("Las contraseñas no coinciden")
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        print("Saving user")
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user