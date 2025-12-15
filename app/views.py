from uuid import uuid4
from django.shortcuts import render, redirect
from . forms import RegistForm
from . models import UserActivateToken
from django.contrib import messages
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def home(request):
    return render(
        request,'base.html'
    )

def regist(request):
    form = RegistForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        token = uuid4()
        user.is_activate = False
        user.save()

        token= uuid4
        expired_at=timezone.now() + timedelta(days=1)

        user_token, created = UserActivateToken.objects.update_or_create(
        user=user,
        defaults={
            'token': token,
            'expired_at': expired_at,
        }
        )
        print("作成されたtoken", user_token.token)
        return redirect('accounts:home')
    
    return render(
        request,'accounts/regist.html',
        context={'regist_form': form,}
    )

def activate_user(request, token):
    activate_form = forms.UserActivateForm(request.POST or None)
    if activate_form.is_valid():
        UserActivateToken.objects.activate_user_by_token(token) #ユーザー有効化
        messages.success(request, '登録しました')
    activate_form.initial['token'] = token
    return render(
        request, 'accounts/activate_user.html', context={
            'activate_form': activate_form,
        }
    )
def user_login(request):
    login_form = forms.LoginForm(request.POST or None)
    if login_form.is_valid():
        email = login_form['email']
        password = login_form['password']
        user = authenticate(email=email, password=password)
        if user:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.warning(request, 'ログインに失敗しました')
    return render(
        request, 'accounts/user_login.html', context={
            'login_form': login_form,
        }
    )

@login_required
def user_logout(request):
    logout(request)
    return redirect('accounts:home')
