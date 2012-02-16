# -*- coding: utf-8 -*-

"""
Forms used in this web.
"""
from django import forms
from django.forms import ModelForm


class CandidateForm(forms.Form):
    name = forms.CharField(max_length=255)
    abbreviation = forms.CharField(max_length=255)
    description = forms.TextField(help_text="Programa electoral")
    image = forms.URLField()

class LoginForm(forms.Form):
    user = forms.EmailField(max_length=255)
    password = forms.PasswordField(max_length=255)

    def clean_user(self):
        pass

    def clean_password(self):
        pass

class RegisterForm(forms.Form):
    user = forms.EmailField(max_length=255)
    password = forms.PasswordField(max_length=255)
    password_rep = forms.PasswordField(max_length=255)

    def clean_user(self):
        pass

    def clean_password(self):
        pass



class CommentForm(forms.Form):
    name = forms.CharField(max_length=255)
    text = forms.TextField()

#class VoteForm(forms.Form):
#   stars # CHOICEFIELD???
