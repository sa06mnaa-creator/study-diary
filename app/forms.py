from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class RegistForm(forms.ModelForm):
    birthday = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    confirm_password = forms.CharField(
        label='パスワード再入力',widget=forms.PasswordInput()
    )
    
    class Meta():
        model = User
        fields = ('username','birthday','email','password')
        labels ={
            'username': '名前',
            'birthday': '生年月日',
            'email': 'メールアドレス',
            'password': 'パスワード',
        }
        widgets = {
            'birthday': forms.NumberInput(attrs={
                'min':1920-00-00
            }),
            'password': forms.PasswordInput()
        }

        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data['password']
            confilm_password = cleaned_data['confirm_password']
            if password != confilm_password:
              self.add_error('password','パスワードが一致しません')
            try:
               validate_password(password, self.instance)
            except ValidationError as e:
               self.add_error('password', e)
            return cleaned_data
        def save(self, commit=False):
            user = super().save(commit=False)
            user.set_password(self.cleaned_data['password'])
            if commit:
                user.save()
            return user