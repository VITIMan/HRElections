# -*- coding: utf-8 -*-

"""
Forms used in this web.
"""
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
#from django.core.exceptions import DoesNotExist

class CandidateForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=255, widget=forms.TextInput(attrs={'class':'span5', 'placeholder':'Nombre del partido'}))
    abbreviation = forms.CharField(min_length=1, max_length=255, widget=forms.TextInput(attrs={'class':'span5', 'placeholder':'Siglas del partido'}))
    description = forms.CharField(min_length=1, widget=forms.Textarea(attrs={'class':'span5', 'rows':'15','placeholder':'Tus ideales, tus propuestas'}))
    image = forms.URLField(min_length=1, widget=forms.TextInput(attrs={'class':'span5', 'placeholder':'Enlace a la imagen'}))
    editing = forms.CharField(label='nop', widget=forms.HiddenInput)

class LoginForm(forms.Form):
    user = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class':'span5', 'placeholder':'Tu email'}) )
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class':'span5', 'placeholder':'Tu contraseña'}))

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get('user')
        password = cleaned_data.get('password')
        try:
            user=User.objects.get(username__exact=username)
            if not user.check_password(password):
                raise forms.ValidationError('Usuario o contraseña incorrecta')
        except User.DoesNotExist:
            raise forms.ValidationError('Usuario o contraseña incorrecta')
        return cleaned_data

class RegisterForm(forms.Form):
    user = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class':'span5'}))
    password = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class':'span5'}))
    password_rep = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class':'span5'}))

    def clean_user(self):
        value = self.cleaned_data['user']
        try:
            User.objects.get(username__exact=value)
        except User.DoesNotExist:
            return value
        raise forms.ValidationError('Usuario existente')

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        value = self.cleaned_data['password']
        rep_value = cleaned_data.get('password_rep')
        if value != rep_value:
            raise forms.ValidationError('Deben coincidir las contraseñas')
        else:
            return cleaned_data


class CommentForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=255, widget=forms.TextInput(attrs={'placeholder':'Nombre'}))
    text = forms.CharField(min_length=1, widget=forms.Textarea(attrs={'rows':'3','placeholder':'Comenta...'}))

#class VoteForm(forms.Form):
#   stars # CHOICEFIELD???
