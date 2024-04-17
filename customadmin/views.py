from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Prefetch
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from cinema.models import Movie, Cinema
from users.models import CustomUser
from .forms import *
from other.models import Promotions, News
from banner.models import MainBannerSettings, NewsBannerSettings, BackBanner
from .tasks import send_spam_emails, send_selected_users


def is_admin(user):
    return user.is_authenticated and user.is_staff


def stats(request):
    count_users = CustomUser.objects.count()

    count_users_ukrainian = CustomUser.objects.filter(language='u').count()
    count_users_english = CustomUser.objects.filter(language='r').count()
    last_logins = CustomUser.objects.exclude(last_login=None).values_list('last_login', flat=True)

    # Convert last login times to timestamps
    last_logins_timestamps = [(login - timezone.datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds() for login in
                              last_logins]
    context = {
        'title': 'Страница статистики',
        'user_count': count_users,
        'percentage_ukrainian': (count_users_ukrainian / count_users) * 100 if count_users > 0 else 0,
        'percentage_english': (count_users_english / count_users) * 100 if count_users > 0 else 0,
        'last_logins': last_logins_timestamps,
    }

    return render(request, 'customadmin/stats.html', context=context)

@login_required
@user_passes_test(is_admin)
def banner(request):

    main_formset = MainBannerFormSet(queryset=MainBanner.objects.all(), prefix='main')
    another_formset = DownBannerFormSet(queryset=NewsBanner.objects.all(), prefix='another')

    context = {
        'title': 'Страница баннеров',
        'main_formset': main_formset,
        'another_formset': another_formset,
    }
    return render(request, 'customadmin/banner.html', context)


@login_required
@user_passes_test(is_admin)
def save_main_banner(request):
    if request.method == 'POST':
        formset = MainBannerFormSet(request.POST, request.FILES, prefix='main')

        if formset.is_valid():
            formset_instance = MainBannerSettings.objects.create(
                speed=request.POST.get('top-time-active'),
                active=request.POST.get('active') == 'on'
            )

            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    # If the form is marked for deletion, delete the associated instance
                    if form.instance.pk:
                        form.instance.delete()
                else:
                    form_banner = form.save(commit=False)
                    form_banner.settings = formset_instance
                    form_banner.save()

            return redirect('adminlte:banner')
        else:
            print(formset.errors)


@login_required
@user_passes_test(is_admin)
def save_another_banner(request):
    if request.method == 'POST':
        formset = DownBannerFormSet(request.POST, request.FILES, prefix='another')

        if formset.is_valid():
            formset_instance = NewsBannerSettings.objects.create(
                speed=request.POST.get('bottom-time-active'),
                active=request.POST.get('active') == 'on'
            )

            for form in formset:
                if form.cleaned_data.get('DELETE'):
                    # If the form is marked for deletion, delete the associated instance
                    if form.instance.pk:
                        form.instance.delete()
                else:
                    form_banner = form.save(commit=False)
                    form_banner.settings = formset_instance
                    form_banner.save()

            return redirect('adminlte:banner')
        else:
            print(formset.errors)


@login_required
@user_passes_test(is_admin)
@csrf_exempt
def save_back_banner(request):
    if request.method == 'POST' and request.FILES.get('back_banner_photo'):
        back_banner_photo = request.FILES['back_banner_photo']
        choice = request.POST.get('choice', 'd')  # Default to 'd' if choice is not provided
        back_banner_object = BackBanner(image=back_banner_photo, choice=choice)
        back_banner_object.save()
        return JsonResponse({'success': True, 'image_url': back_banner_object.image.url, 'choice': back_banner_object.choice})
    else:
        return JsonResponse({'success': False})


@login_required
@user_passes_test(is_admin)
def films(request):
    film = Movie.objects.all()

    context = {
        'title': 'Список фильмов',
        'movie': film
    }
    return render(request, 'customadmin/films.html', context=context)


@login_required
@user_passes_test(is_admin)
def page_film(request):
    if request.method == 'POST':
        films_form = FilmsForm(request.POST, request.FILES)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES)
        if films_form.is_valid() and gallery_formset.is_valid():
            film_instance = films_form.save(commit=False)
            film_instance.title_en = films_form.cleaned_data['title']
            film_instance.description_en = films_form.cleaned_data['description']
            gallery_instance = Gallery.objects.create(title=film_instance.title)
            film_instance.gallery = gallery_instance
            film_instance.save()

            for form in gallery_formset:
                print(form.cleaned_data)
                if form.cleaned_data.get('image'):
                    gallery_image = form.save(commit=False)
                    gallery_image.gallery = gallery_instance
                    gallery_image.save()

            return redirect('adminlte:film')
    else:
        films_form = FilmsForm()
        gallery_formset = GalleryImageFormSet(queryset=Gallery.objects.none())

    return render(request, 'customadmin/add_film.html',
                  {'title': 'Добавление фильма', 'name': 'фильма', 'form': films_form,
                   'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def edit_film(request, film_id):
    film_instance = get_object_or_404(Movie, pk=film_id)
    if request.method == 'POST':
        films_form = FilmsForm(request.POST, request.FILES, instance=film_instance, initial={'type': film_instance.type}
                               )
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES, queryset=GalleryImage.objects.filter(
            gallery=film_instance.gallery))

        if films_form.is_valid() and gallery_formset.is_valid():
            cinema_instance = films_form.save()

            gallery_instances = gallery_formset.save(commit=False)

            for form in gallery_formset.deleted_forms:
                form.instance.delete()

            for gallery_instance in gallery_instances:
                gallery_instance.gallery = cinema_instance.gallery
                gallery_instance.save()

            return redirect('adminlte:film')
        else:
            print(films_form.errors)
            print(gallery_formset.errors)
    else:
        films_form = FilmsForm(instance=film_instance)
        gallery_formset = GalleryImageFormSet(queryset=GalleryImage.objects.filter(gallery=film_instance.gallery))

    return render(request, 'customadmin/edit_films.html', {'title': 'Редактирование кинотеатра',
                                                             'film_instance': film_instance,
                                                             'form': films_form, 'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def cinemas(request):
    cinema = Cinema.objects.all()

    context = {
        'title': 'Страница кинотеатров',
        'cinema': cinema
    }

    return render(request, 'customadmin/cinema.html', context=context)


@login_required
@user_passes_test(is_admin)
def cinema_page(request):
    if request.method == 'POST':
        cinema_form = CinemaForm(request.POST, request.FILES)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES)
        if cinema_form.is_valid() and gallery_formset.is_valid():

            film_instance = cinema_form.save(commit=False)
            film_instance.title_en = cinema_form.cleaned_data['title']
            film_instance.description_en = cinema_form.cleaned_data['description']
            gallery_instance = Gallery.objects.create(title=film_instance.title)
            film_instance.gallery = gallery_instance
            film_instance.save()

            for form in gallery_formset:
                if form.cleaned_data.get('image'):
                    gallery_image = form.save(commit=False)
                    gallery_image.gallery = gallery_instance
                    gallery_image.save()

            return redirect('adminlte:cinema')
    else:
        cinema_form = CinemaForm()
        gallery_formset = GalleryImageFormSet(queryset=Gallery.objects.none())

    return render(request, 'customadmin/add_cinema.html',
                  {'title': 'Добавление кинотеатра', 'name': 'кинотеатра', 'form': cinema_form,
                   'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def edit_cinema(request, cinema_id):
    cinema_instance = get_object_or_404(Cinema, pk=cinema_id)
    if request.method == 'POST':
        cinema_form = CinemaForm(request.POST, request.FILES, instance=cinema_instance)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES, queryset=GalleryImage.objects.filter(
            gallery=cinema_instance.gallery))

        if cinema_form.is_valid() and gallery_formset.is_valid():
            cinema_instance = cinema_form.save()
            cinema_instance.title_en = cinema_form.cleaned_data['title']
            cinema_instance.description_en = cinema_form.cleaned_data['description']

            gallery_instances = gallery_formset.save(commit=False)

            for form in gallery_formset.deleted_forms:
                form.instance.delete()

            for gallery_instance in gallery_instances:
                gallery_instance.gallery = cinema_instance.gallery
                gallery_instance.save()

            return redirect('adminlte:cinema')
        else:
            print(cinema_form.errors)
            print(gallery_formset.errors)
    else:
        cinema_form = CinemaForm(instance=cinema_instance)
        gallery_formset = GalleryImageFormSet(queryset=GalleryImage.objects.filter(gallery=cinema_instance.gallery))

    return render(request, 'customadmin/edit_cinema.html', {'title': 'Редактирование кинотеатра',
                                                             'cinema_instance': cinema_instance,
                                                             'form': cinema_form, 'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def delete_cinema(request, cinema_id):
    if request.method == 'POST':
        cinema = Cinema.objects.get(id=cinema_id)
        cinema.delete()
        return redirect('adminlte:cinema')
    else:
        return redirect('adminlte:cinema')


@login_required
@user_passes_test(is_admin)
def cinema_hall(request):
    if request.method == 'POST':
        cinema_hall_form = CinemaHallForm(request.POST, request.FILES)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES)
        if cinema_hall_form.is_valid() and gallery_formset.is_valid():
            film_instance = cinema_hall_form.save(commit=False)
            gallery_instance = Gallery.objects.create(title=film_instance.title)
            film_instance.gallery = gallery_instance
            film_instance.save()

            for form in gallery_formset:
                print(form.cleaned_data)
                if form.cleaned_data.get('image'):
                    gallery_image = form.save(commit=False)
                    gallery_image.gallery = gallery_instance
                    gallery_image.save()

            return redirect('success_url')
        else:
            print(cinema_hall_form.errors)
            print(gallery_formset.errors)
    else:
        cinema_hall_form = CinemaHallForm()
        gallery_formset = GalleryImageFormSet(queryset=Gallery.objects.none())

    return render(request, 'customadmin/card_hall.html',
                  {'title': 'Добавление зала', 'name': 'зала', 'form': cinema_hall_form,
                   'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def news(request):
    all_news = News.objects.all()
    
    context = {
        'title': 'Страница новостей',
        'news': all_news
    }
    
    return render(request, 'customadmin/news.html', context=context)


@login_required
@user_passes_test(is_admin)
def news_add(request):
    if request.method == 'POST':
        news_add_form = NewsForm(request.POST, request.FILES)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES)
        if news_add_form.is_valid() and gallery_formset.is_valid():
            film_instance = news_add_form.save(commit=False)
            film_instance.title_en = news_add_form.cleaned_data['title']
            film_instance.description_en = news_add_form.cleaned_data['description']
            gallery_instance = Gallery.objects.create(title=film_instance.title)
            film_instance.gallery = gallery_instance
            film_instance.save()

            for form in gallery_formset:
                print(form.cleaned_data)
                if form.cleaned_data.get('image'):
                    gallery_image = form.save(commit=False)
                    gallery_image.gallery = gallery_instance
                    gallery_image.save()

            return redirect('adminlte:news')

    else:
        news_add_form = NewsForm()
        gallery_formset = GalleryImageFormSet(queryset=Gallery.objects.none())

    return render(request, 'customadmin/forms.html',
                  {'title': 'Добавление новости', 'name': 'новости', 'form': news_add_form,
                   'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def edit_news(request, news_id):
    news_instance = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        news_form = NewsForm(request.POST, request.FILES, instance=news_instance)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES,
                                              queryset=GalleryImage.objects.filter(gallery=news_instance.gallery))

        if news_form.is_valid() and gallery_formset.is_valid():
            news_instance = news_form.save()

            gallery_instances = gallery_formset.save(commit=False)

            for form in gallery_formset.deleted_forms:
                form.instance.delete()

            for gallery_instance in gallery_instances:
                gallery_instance.gallery = news_instance.gallery
                gallery_instance.save()

            return redirect('adminlte:news')
        else:
            print(news_form.errors)
            print(gallery_formset.errors)
    else:
        news_form = NewsForm(instance=news_instance)
        gallery_formset = GalleryImageFormSet(queryset=GalleryImage.objects.filter(gallery=news_instance.gallery))

    return render(request, 'customadmin/edit_other_page.html', {'title': 'Редактирование новостей',
                                                            'news_instance': news_instance, 'form': news_form,
                                                            'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def sells(request):

    all_sells = Promotions.objects.all()

    context = {
        'title': 'Страница акций',
        'sells': all_sells
    }
    
    return render(request, 'customadmin/sells.html', context=context)


@login_required
@user_passes_test(is_admin)
def add_sells(request):
    if request.method == 'POST':
        sells_form = SellsForm(request.POST, request.FILES)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES)
        if sells_form.is_valid() and gallery_formset.is_valid():
            film_instance = sells_form.save(commit=False)
            film_instance.title_en = sells_form.cleaned_data['title']
            film_instance.description_en = sells_form.cleaned_data['description']
            gallery_instance = Gallery.objects.create(title=film_instance.title)
            film_instance.gallery = gallery_instance
            film_instance.save()

            for form in gallery_formset:
                print(form.cleaned_data)
                if form.cleaned_data.get('image'):
                    gallery_image = form.save(commit=False)
                    gallery_image.gallery = gallery_instance
                    gallery_image.save()

            return redirect('adminlte:sells')
    else:
        sells_form = SellsForm()
        gallery_formset = GalleryImageFormSet(queryset=Gallery.objects.none())

    return render(request, 'customadmin/forms.html',
                  {'title': 'Добавление акции', 'name': 'акции', 'form': sells_form,
                   'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def edit_sells(request, sells_id):
    sells_instance = get_object_or_404(Promotions, pk=sells_id)
    if request.method == 'POST':
        sells_form = SellsForm(request.POST, request.FILES, instance=sells_instance)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES,
                                              queryset=GalleryImage.objects.filter(gallery=sells_instance.gallery))

        if sells_form.is_valid() and gallery_formset.is_valid():
            news_instance = sells_form.save()

            gallery_instances = gallery_formset.save(commit=False)

            for form in gallery_formset.deleted_forms:
                form.instance.delete()

            for gallery_instance in gallery_instances:
                gallery_instance.gallery = news_instance.gallery
                gallery_instance.save()

            return redirect('adminlte:sells')
        else:
            print(sells_form.errors)
            print(gallery_formset.errors)
    else:
        sells_form = SellsForm(instance=sells_instance)
        gallery_formset = GalleryImageFormSet(queryset=GalleryImage.objects.filter(gallery=sells_instance.gallery))

    return render(request, 'customadmin/edit_other_page.html', {'title': 'Редактирование новостей',
                                                            'sells_instance': sells_instance, 'form': sells_form,
                                                            'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def pages(request):

    all_pages = Pages.objects.all()
    
    context = {
        'title': 'Страницы',
        'pages': all_pages
    }
    
    return render(request, 'customadmin/pages.html', context=context)


@login_required
@user_passes_test(is_admin)
def main_page(request, main_page_id=1):
    main_page_instance = get_object_or_404(MainPage, pk=main_page_id)
    if request.method == 'POST':
        main_page_form = MainPageForm(request.POST, instance=main_page_instance)

        if main_page_form.is_valid():
            main_page_form.save()
        else:
            print(main_page_form.errors)

    else:
        main_page_form = MainPageForm(instance=main_page_instance)

    return render(request, 'customadmin/main_page.html', context={'title': 'Главная страница', 'main_page_instance': main_page_instance, 'form': main_page_form})


@login_required
@user_passes_test(is_admin)
def contacts(request):
    context = {
        'title': 'Контакты'
    }

    return render(request, 'customadmin/contacts.html', context=context)


@login_required
@user_passes_test(is_admin)
def new_page(request):
    if request.method == 'POST':
        new_page_form = PagesForm(request.POST, request.FILES)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES)
        if new_page_form.is_valid() and gallery_formset.is_valid():
            film_instance = new_page_form.save(commit=False)
            film_instance.title_en = new_page_form.cleaned_data['title']
            film_instance.description_en = new_page_form.cleaned_data['description']
            gallery_instance = Gallery.objects.create(title=film_instance.title)
            film_instance.gallery = gallery_instance
            film_instance.save()

            for form in gallery_formset:
                if form.cleaned_data.get('image'):
                    gallery_image = form.save(commit=False)
                    gallery_image.gallery = gallery_instance
                    gallery_image.save()

            return redirect('adminlte:pages')
        else:
            print(new_page_form.errors)
            print(gallery_formset.errors)
    else:
        new_page_form = PagesForm()
        gallery_formset = GalleryImageFormSet(queryset=Gallery.objects.none())
    return render(request, 'customadmin/add_page.html',
                  {'title': 'Добавление страницы', 'name': 'страницы', 'form': new_page_form, 'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def edit_pages(request, page_id):
    page_instance = get_object_or_404(Pages, pk=page_id)
    if request.method == 'POST':
        page_form = PagesForm(request.POST, request.FILES, instance=page_instance)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES,
                                              queryset=GalleryImage.objects.filter(gallery=page_instance.gallery))

        if page_form.is_valid() and gallery_formset.is_valid():
            page_instance = page_form.save()

            gallery_instances = gallery_formset.save(commit=False)

            for form in gallery_formset.deleted_forms:
                form.instance.delete()

            for gallery_instance in gallery_instances:
                gallery_instance.gallery = page_instance.gallery
                gallery_instance.save()

            return redirect('adminlte:pages')
        else:
            print(page_form.errors)
            print(gallery_formset.errors)
    else:
        page_form = PagesForm(instance=page_instance)
        gallery_formset = GalleryImageFormSet(queryset=GalleryImage.objects.filter(gallery=page_instance.gallery))

    return render(request, 'customadmin/edit_other_page.html', {'title': 'Редактирование новостей',
                                                            'page_instance': page_instance, 'form': page_form,
                                                            'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def users(request):

    all_users = CustomUser.objects.select_related().all()
    
    context = {
        'title': 'Страница пользователей',
        'users': all_users
    }
    
    return render(request, 'customadmin/users.html', context=context)


@login_required
@user_passes_test(is_admin)
def edit_user(request, user_id):
    user_instance = get_object_or_404(CustomUser, pk=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user_instance)
        if form.is_valid():
            # Сохраняем данные пользователя из формы
            form.save()

            # Обработка нового пароля, если он был введен
            new_password = request.POST.get('password')
            if new_password:
                # Хешируем новый пароль и сохраняем его
                user_instance.password = make_password(new_password)
                user_instance.save()

            return redirect('adminlte:users')
        else:
            print(form.errors)
    else:
        pass

    context = {
        'title': 'Редактация пользователя',
        'user': user_instance
    }

    return render(request, 'customadmin/edit_user.html', context=context)


@login_required
@user_passes_test(is_admin)
def spam(request):
    files = Spam.objects.select_related().all()
    all_users = CustomUser.objects.all()
    if request.method == 'POST':
        form = SpamForm(request.POST, request.FILES)
        if form.is_valid():
            selected_file = form.cleaned_data['file_name']
            if request.POST.get('recipientType') == 'allUsers':
                recipients = [user.email for user in all_users if user.email]
                send_spam_emails.delay(selected_file, recipients)
                return redirect('adminlte:spam')
            elif request.POST.get('recipientType') == 'selective':
                # Получаем выбранных пользователей из формы
                selectedUsers = request.POST.get('selectedUsers[]').split(',')
                # Отправляем письма выбранным пользователям
                send_selected_users.delay(selected_file, selectedUsers)
                return JsonResponse({'message': 'Рассылка только выбранным пользователям запущена.'})
            else:
                return JsonResponse({'error': 'Некорректный тип получателей.'}, status=400)
        else:
            print(form.errors)
            return JsonResponse({'error': 'Ошибка валидации формы.'}, status=400)
    else:
        form = SpamForm()

    context = {
        'title': 'Страница рассылки',
        'files': files,
        'form': form,
        'users': all_users
    }

    return render(request, 'customadmin/spam.html', context=context)


@login_required
@user_passes_test(is_admin)
@csrf_exempt
def save_email_file(request):
    if request.method == 'POST' and request.FILES.get('emailFile'):
        email_file = request.FILES['emailFile']
        spam_object = Spam(file_name=email_file.name, file=email_file)
        spam_object.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
