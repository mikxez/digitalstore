from django import forms
from django.core.validators import RegexValidator
from django_svg_image_form_field import SvgAndImageFormField
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        exclude = []
        field_classes = {
            'icon': SvgAndImageFormField
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'contact__section-input'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'contact__section-input'
    }))


class RegisterForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'contact__section-input',
            'placeholder': 'Введите имя пользователя'
        }),
        error_messages={
            'required': 'Это поле обязательно для заполнения.'
        }
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'contact__section-input',
            'placeholder': 'Введите пароль'
        }),
        error_messages={
            'required': 'Это поле обязательно для заполнения.'
        }
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'contact__section-input',
            'placeholder': 'Повторите пароль'
        }),
        error_messages={
            'required': 'Это поле обязательно для заполнения.'
        }
    )

    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'contact__section-input',
            'placeholder': 'Введите ваше имя'
        }),
        error_messages={
            'required': 'Это поле обязательно для заполнения.'
        }
    )

    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'contact__section-input',
            'placeholder': 'Введите ваше фамилия'
        }),
        error_messages={
            'required': 'Это поле обязательно для заполнения.'
        }
    )

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'contact__section-input',
            'placeholder': 'Введите вашу почту'
        }),
        error_messages={
            'required': 'Это поле обязательно для заполнения.',
            'invalid': 'Введите корректный адрес электронной почты.'
        }
    )

    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите номер телефона (например, +998901234567)',
            'class': 'contact__section-input'
        }),
        validators=[RegexValidator(
            regex=r'^\+998\d{9}$',
            message='Введите корректный номер телефона Узбекистана, начиная с +998'
        )],
        error_messages={
            'required': 'Это поле обязательно для заполнения.',
            'invalid': 'Введите корректный номер телефона.'
        }
    )

    photo = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'contact__section-input',
            'placeholder': 'Загрузите фото'
        }),
        error_messages={
            'invalid': 'Файл не поддерживается.'
        }
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'photo')

class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'telegram']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'contact__section-input',
                'placeholder': 'Имя получателя',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'contact__section-input',
                'placeholder': 'Фамилия получателя'
            }),

            'telegram': forms.TextInput(attrs={
                'class': 'contact__section-input',
                'placeholder': 'Телеграм получателя'
            })
        }


class ShippingForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ('region', 'city', 'address', 'phone', 'comment')
        widgets = {
            'region': forms.Select(attrs={
                'class': 'contact__section-input',
            }),
            'city': forms.Select(attrs={
                'class': 'contact__section-input',
            }),

            'address': forms.TextInput(attrs={
                'class': 'contact__section-input',
                'placeholder': 'Адрес (ул. дом. кв)'
            }),

            'phone': forms.TextInput(attrs={
                'class': 'contact__section-input',
                'placeholder': 'Номер телефона',
                'type': 'phone'
            }),

            'comment': forms.Textarea(attrs={
                'class': 'contact__section-input',
                'placeholder': 'Комментарий к заказу',
            })

        }

class EditAccountForm(UserChangeForm):
    first_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Имя',
    }))

    last_name = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Фамилия',
    }))

    email = forms.EmailField(required=False ,widget=forms.EmailInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Почта',
    }))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class EditProfileForm(forms.ModelForm):
    phone = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Номер',
    }))

    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Город',
    }))

    street = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Улица',
    }))

    home = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Дом',
    }))

    flat = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class': 'contact__section-input',
        'placeholder': 'Квартира',
    }))

    class Meta:
        model = Profiles
        fields = ('phone', 'city', 'street', 'home', 'flat')
