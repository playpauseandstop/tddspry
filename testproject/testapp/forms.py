from django import forms
from django.contrib import auth
from django.utils.translation import ugettext_lazy as _


__all__ = ('LoginForm', )


class LoginForm(forms.Form):

    username = forms.CharField(label=_('Username'), max_length=30,
        required=True)
    password = forms.CharField(label=_('Password'), max_length=255,
        required=True, widget=forms.PasswordInput)

    def clean_password(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not username or not password:
            return password

        user = auth.authenticate(username=username, password=password)

        if user is None:
            raise forms.ValidationError, \
                'Please, enter valid username and password.'

        if not user.is_active:
            raise forms.ValidationError, 'Your account is disabled.'

        self.user_cache = user
        return password

    def save(self, request):
        return auth.login(request, self.user_cache)
