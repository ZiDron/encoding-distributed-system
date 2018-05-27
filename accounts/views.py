from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


from urllib.parse import urlparse

from django.shortcuts import redirect, render_to_response
from django.contrib import auth
from django.template.context_processors import csrf
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .special_func import get_next_url


class ELoginView(View):

    def get(self, request):
    #     # если пользователь авторизован, то делаем редирект на главную страницу
    #     if auth.get_user(request).is_authenticated:
    #         return redirect('/')
    #     else:
     # Иначе формируем контекст с формой авторизации и отдаём страницу
    # с этим контекстом.
    # работает, как для url - /admin/login/ так и для /accounts/login/
        context = create_context_username_csrf(request)
        return render_to_response('accounts/login.html', context=context)

    def post(self, request):
        # получив запрос на авторизацию
        form = AuthenticationForm(request, data=request.POST)

        # проверяем правильность формы, что есть такой пользователь
        # и он ввёл правильный пароль
        if form.is_valid():
            # в случае успеха авторизуем пользователя
            auth.login(request, form.get_user())
            # получаем предыдущий url
            next = urlparse(get_next_url(request)).path
            # и если пользователь из числа персонала и заходил через url /admin/login/
            # то перенаправляем пользователя в админ панель
            if next == '/admin/login/' and request.user.is_staff:
                return redirect('/admin/')
            # иначе делаем редирект на предыдущую страницу,
            # в случае с /accounts/login/ произойдёт ещё один редирект на главную страницу
            # в случае любого другого url, пользователь вернётся на данный url
            return redirect(next)

        # если данные не верны, то пользователь окажется на странице авторизации
        # и увидит сообщение об ошибке
        context = create_context_username_csrf(request)
        context['login_form'] = form

        return render_to_response('accounts/login.html', context=context)


# вспомогательный метод для формирования контекста с csrf_token
# и добавлением формы авторизации в этом контексте
def create_context_username_csrf(request):
    context = {}
    context.update(csrf(request))
    context['login_form'] = AuthenticationForm
    return context