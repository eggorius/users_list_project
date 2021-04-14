import django.forms as forms
from django.contrib.auth.models import User


class LoginForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput, label='Пароль')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователе с именем {username} не существует.')
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('Неверный пароль')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'password']


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Логин'
        self.fields['password'].label = 'Пароль'
        self.fields['confirm_password'].label = 'Поддтвердите пароль'
        self.fields['email'].required = True

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Пользователь с данной электронной почтой уже существует.')
        return email

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'confirm_password']






