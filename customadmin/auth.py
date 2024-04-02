from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff:
                login(request, user)
                print(request.session)
                return redirect('adminlte:banner')
            else:
                login(request, user)
                return redirect('adminlte:banner')
        else:
            return render(request, 'customadmin/login.html', {'error': 'Неправильний логін або пароль'})
    return render(request, 'customadmin/login.html')
