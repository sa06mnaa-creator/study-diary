from django.shortcuts import render, redirect
from . forms import RegistForm

def home(request):
    return render(
        request,'base.html'
    )

def regist(request):
    form = RegistForm(request.POST or None)
    if form.is_valid():
        form.save(commit=True)
        return redirect('accounts:home')
    return render(
        request,'accounts/regist.html',context={
            'regist_form': form,
        }
    )