from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .forms import CardForm, LoginUserForm, CardSearchForm, FileUploadForm
from .models import Card
from .utils import get_nominal, process_txt_file


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'gift_card/login.html'
    extra_context = {'title': "Авторизация"}

    def get_success_url(self):
        if self.request.user.is_staff:
            return reverse_lazy('show')
        else:
            return reverse_lazy('card')


@login_required
def input_card(request):
    user = request.user
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            number = form.cleaned_data['number']

            new_card = Card.objects.filter(number=number).first()
            if new_card:
                new_card.user = user
                new_card.save()
            else:
                new_card = Card()
                new_card.user = user
                new_card.number = number
                new_card.nominal = get_nominal(number)

                new_card.save()
            messages.success(request, f'Карта {number} отправлена')
        else:
            count_card = Card.objects.filter(user=user).count()
            return render(request, 'gift_card/gift-card.html', {'form': form, 'count_card': count_card})

    form = CardForm()
    count_card = Card.objects.filter(user=user).count()
    return render(request, 'gift_card/gift-card.html', {'form': form, 'count_card': count_card})


@login_required
def show_card(request):
    if request.user.is_staff:
        # Проверяем параметры запроса и обновляем форму фильтрации с учетом них
        user_id = request.GET.get('user', None)
        nominal = request.GET.get('nominal', None)
        number = request.GET.get('number', None)
        initial = {'user': user_id, 'nominal': nominal, 'number': number}
        form = CardSearchForm(initial=initial)

        # Применяем фильтры
        filter_params = {}
        if user_id:
            filter_params['user'] = User.objects.get(id=user_id)
        if nominal:
            filter_params['nominal'] = nominal
        if number:
            filter_params['number'] = number

        form_file = FileUploadForm()

        table = Card.objects.filter(**filter_params)

        paginator = Paginator(table, 20)

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'gift_card/show-card.html', {
            "form": form,
            "form_file": form_file,
            "page_obj": page_obj,
            "paginator": paginator,
        })

    raise PermissionDenied("Только HR директор может просматривать эту страницу")


def add_card(request):
    if request.user.is_staff:
        if request.method == 'POST':
            form = FileUploadForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = request.FILES['file']
                if uploaded_file.name.endswith('.txt'):
                    count_card = process_txt_file(uploaded_file, request.user)
                    if count_card["count_new"] > 0:
                        messages.error(request, f'В Офис добавлено новых карт: {count_card["count_new"]} шт.')
                    messages.error(request, f'В Офис добавлено карт: {count_card["count_edit"]} шт.')
                    return redirect('show')
                else:
                    messages.error(request, 'Ошибка загрузки файла. Выберите текстовый файл.txt')
        return redirect('show')
    raise PermissionDenied("Только HR директор может просматривать эту страницу")


def logout_user(request):
    logout(request)
    return redirect('login')


def custom_permission_denied(request, exception):
    error_message = str(exception)
    return render(request, 'gift_card/403.html', status=403, context={"error_message": error_message})


def handler404(request, exception):
    return render(request, 'gift_card/404.html', status=404)
