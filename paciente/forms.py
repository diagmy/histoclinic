from django import forms
from .models import *

class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        widgets={
            'first_name':forms.TextInput(
                  attrs={'placeholder': 'First Name','class':'form-control placeholder-no-fix'}),
            'last_name': forms.TextInput(
                attrs={'placeholder': 'Last Name', 'class': 'form-control placeholder-no-fix'}),
            'username': forms.TextInput(
                attrs={'placeholder': 'Username', 'class': 'form-control placeholder-no-fix'}),
            'email': forms.TextInput(
                attrs={'placeholder': 'Email', 'class': 'form-control placeholder-no-fix','type':'email'}),
            'password': forms.TextInput(
                attrs={'placeholder': 'Password', 'class': 'form-control placeholder-no-fix,'}),
        }

class SignupFormExtend(forms.ModelForm):

    class Meta:
          model = UserProfile
          fields = ('state',)
          widgets={


          }

    # def clean_username(self):
    #     username = self.cleaned_data["username"]
    #     if not alnum_re.search(username):
    #         raise forms.ValidationError(u'Usernames can only contain letters, numbers and underscores.')
    #     if RegistrationProfile.objects.filter(username__iexact=username).exists() \
    #         or User.objects.filter(username__iexact=username).exists():
    #         raise forms.ValidationError(u'This username is already taken. Please choose another.')
    #     return username
    #
    # def clean_email(self):
    #     email = self.cleaned_data["email"]
    #     if RegistrationProfile.objects.filter(email__iexact=email).exists() \
    #         or User.objects.filter(email__iexact=email).exists():
    #         raise forms.ValidationError(u'This email address is already in use. Please choose another.')
    #     return email
    #
    # def clean(self):
    #     if "password" in self.cleaned_data and "password_confirm" in self.cleaned_data:
    #         if self.cleaned_data["password"] != self.cleaned_data["password_confirm"]:
    #             raise ValidationError(u'You must type the same password each time.')
    #     return self.cleaned_data





class AntecedentesFamiliaresPatologicosForm(forms.Form):


    class Meta:
        model = AntecedentesFamiliaresPatologicos
        field = {'parentesco',}


