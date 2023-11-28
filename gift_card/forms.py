from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


from .models import Card
from .utils import not_valid_number


class LoginUserForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'lf--input',
                                                     'placeholder': 'Пользователь',
                                                     "autofocus": False})

        self.fields['password'].widget.attrs.update({'class': 'lf--input',
                                                     'placeholder': 'Пароль'})


class CardForm(forms.ModelForm):

    class Meta:
        model = Card
        fields = ['number']
        widgets = {
            'number': forms.TextInput(
                attrs={'class': 'lf--input custom-class',
                       'placeholder': 'Номер карты',
                       'autocomplete': 'off',
                       })
        }
        error_messages = {
            'number': {
                'required': 'Вы не ввели номер карты',
            }
        }

    def clean_number(self):
        number = self.cleaned_data['number'].strip()

        not_valid_info = not_valid_number(number)
        if not_valid_info:
            raise forms.ValidationError(not_valid_info)

        return number


class CardSearchForm(forms.Form):
    user = forms.ModelChoiceField(
        queryset=User.objects.all(),
        empty_label="Все магазины",
        required=False,
        widget=forms.Select(attrs={'class': 'lf--input'})
    )
    number = forms.CharField(
        max_length=16,
        required=False,
        widget=forms.TextInput(attrs={'class': 'lf--input number',
                                      'placeholder': 'Номер карты'})
    )
    nominal = forms.ChoiceField(
        choices=[(None, 'Номинал'), (500, '500'), (1000, '1000'), (2000, '2000'),
                 (3000, '3000'), (4000, '4000'), (5000, '5000')],
        required=False,
        widget=forms.Select(attrs={'class': 'lf--input'})

    )


class FileUploadForm(forms.Form):
    file = forms.FileField()
