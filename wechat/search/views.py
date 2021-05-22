from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Links
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def index(request):
    linklist = Links.objects.all()
    return render(request, 'search/index.html', {'linklist': linklist})


def logins(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            message = "用户名或密码错误!"
            return render(request, 'search/login.html', locals())
    return render(request, 'search/login.html')


def regist(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        email = request.POST.get("email")
        if password1 != password2:
            message1 = '两次输入的密码不一样！'
            return render(request, 'search/regist.html', locals())
        else:
            if(User.objects.filter(username=username)):
                message3 = '用户已经存在，请重新选择用户名！'
                return render(request, 'search/regist.html', locals())

        cuser = User.objects.create_user(
            username=username, password=password1, email=email)
        cuser.save()
        return redirect('../login/')
    return render(request, 'search/regist.html')

def log_out(request):
    logout(request)
    return redirect('/')
