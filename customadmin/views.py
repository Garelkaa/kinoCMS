from django.db.models import Prefetch
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt

from cinema.models import Movie, Cinema
from users.models import CustomUser
from .forms import *
from .forms import NewsForm, SellsForm, CinemaForm, CinemaHallForm, PagesForm, GalleryImageFormSet, SpamForm
from other.models import Promotions, News
from .tasks import send_spam_emails


def is_admin(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_admin)
def stats(request):

    count_users = CustomUser.objects.count()

    context = {
        'title': 'Страница статистики',
        'user_count': count_users
    }
    
    return render(request, 'customadmin/stats.html', context=context)


@login_required
@user_passes_test(is_admin)
def banner(request):

    context = {
        'title': 'Страница баннеров'
    }
    return render(request, 'customadmin/banner.html', context)


@login_required
@user_passes_test(is_admin)
def films(request):
    film = Movie.objects.prefetch_related(
        Prefetch('gallery__galleryimage_set', queryset=GalleryImage.objects.all())
    ).all()

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
            print(films_form.errors)
            print(gallery_formset.errors)
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
        films_form = FilmsForm(request.POST, request.FILES, instance=film_instance, initial={'type': film_instance.type})
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES, queryset=GalleryImage.objects.filter(gallery=film_instance.gallery))

        if films_form.is_valid() and gallery_formset.is_valid():
            cinema_instance = films_form.save()

            # Save the formset
            gallery_instances = gallery_formset.save(commit=False)

            # Delete images marked for deletion
            for form in gallery_formset.deleted_forms:
                form.instance.delete()

            # Save changes to the database
            for gallery_instance in gallery_instances:
                gallery_instance.gallery = cinema_instance.gallery
                gallery_instance.save()

            return redirect('success_url')
        else:
            print(films_form.errors)
            print(gallery_formset.errors)
    else:
        films_form = FilmsForm(instance=film_instance)
        gallery_formset = GalleryImageFormSet(queryset=GalleryImage.objects.filter(gallery=film_instance.gallery))

    return render(request, 'customadmin/edit_films.html', {'title': 'Редактирование кинотеатра',
                                                             'film_instance': film_instance, 'form': films_form, 'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def cinemas(request):
    cinemas = Cinema.objects.prefetch_related(
        Prefetch('gallery__galleryimage_set', queryset=GalleryImage.objects.all())
    ).all()

    context = {
        'title': 'Страница кинотеатров',
        'cinema': cinemas
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
            gallery_instance = Gallery.objects.create(title=film_instance.title)
            film_instance.gallery = gallery_instance
            film_instance.save()

            for form in gallery_formset:
                print("тут" + f"{form.cleaned_data}")
                if form.cleaned_data.get('image'):
                    gallery_image = form.save(commit=False)
                    gallery_image.gallery = gallery_instance
                    gallery_image.save()

            return redirect('success_url')
        else:
            print(f"Cinema: {cinema_form.errors}")
            print(f"Formset: {gallery_formset.errors}")
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
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES, queryset=GalleryImage.objects.filter(gallery=cinema_instance.gallery))

        if cinema_form.is_valid() and gallery_formset.is_valid():
            cinema_instance = cinema_form.save()

            # Save the formset
            gallery_instances = gallery_formset.save(commit=False)

            # Delete images marked for deletion
            for form in gallery_formset.deleted_forms:
                form.instance.delete()

            # Save changes to the database
            for gallery_instance in gallery_instances:
                gallery_instance.gallery = cinema_instance.gallery
                gallery_instance.save()

            return redirect('success_url')
        else:
            print(cinema_form.errors)
            print(gallery_formset.errors)
    else:
        cinema_form = CinemaForm(instance=cinema_instance)
        gallery_formset = GalleryImageFormSet(queryset=GalleryImage.objects.filter(gallery=cinema_instance.gallery))

    return render(request, 'customadmin/edit_cinema.html', {'title': 'Редактирование кинотеатра',
                                                             'cinema_instance': cinema_instance, 'form': cinema_form, 'gallery_formset': gallery_formset})

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
    all_news = News.objects.prefetch_related().all()
    
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
            print(news_add_form.errors)
            print(gallery_formset.errors)
    else:
        news_add_form = NewsForm()
        gallery_formset = GalleryImageFormSet(queryset=Gallery.objects.none())

    return render(request, 'customadmin/forms.html',
                  {'title': 'Добавление новости', 'name': 'новости', 'form': news_add_form,
                   'gallery_formset': gallery_formset})


def edit_news(request, news_id):
    news_instance = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        news_form = NewsForm(request.POST, request.FILES, instance=news_instance)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES,
                                              queryset=GalleryImage.objects.filter(gallery=news_instance.gallery))

        if news_form.is_valid() and gallery_formset.is_valid():
            news_instance = news_form.save()

            # Save the formset
            gallery_instances = gallery_formset.save(commit=False)

            # Delete images marked for deletion
            for form in gallery_formset.deleted_forms:
                form.instance.delete()

            # Save changes to the database
            for gallery_instance in gallery_instances:
                gallery_instance.gallery = news_instance.gallery
                gallery_instance.save()

            return redirect('success_url')
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

    all_sells = Promotions.objects.prefetch_related().all()

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
            print(sells_form.errors)
            print(gallery_formset.errors)
    else:
        sells_form = SellsForm()
        gallery_formset = GalleryImageFormSet(queryset=Gallery.objects.none())

    return render(request, 'customadmin/forms.html',
                  {'title': 'Добавление акции', 'name': 'акции', 'form': sells_form,
                   'gallery_formset': gallery_formset})


def edit_sells(request, sells_id):
    sells_instance = get_object_or_404(Promotions, pk=sells_id)
    if request.method == 'POST':
        sells_form = SellsForm(request.POST, request.FILES, instance=sells_instance)
        gallery_formset = GalleryImageFormSet(request.POST, request.FILES,
                                              queryset=GalleryImage.objects.filter(gallery=sells_instance.gallery))

        if sells_form.is_valid() and gallery_formset.is_valid():
            news_instance = sells_form.save()

            # Save the formset
            gallery_instances = gallery_formset.save(commit=False)

            # Delete images marked for deletion
            for form in gallery_formset.deleted_forms:
                form.instance.delete()

            # Save changes to the database
            for gallery_instance in gallery_instances:
                gallery_instance.gallery = news_instance.gallery
                gallery_instance.save()

            return redirect('success_url')
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

    all_pages = Pages.objects.prefetch_related().all()
    
    context = {
        'title': 'Страницы',
        'pages': all_pages
    }
    
    return render(request, 'customadmin/pages.html', context=context)


@login_required
@user_passes_test(is_admin)
def main_page(request, main_page_id=4):
    main_page_instance = get_object_or_404(MainPage, pk=main_page_id)
    if request.method == 'POST':
        main_page_form = MainPageForm(request.POST, instance=main_page_instance)

        if main_page_form.is_valid() :
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
            new_page_instance = new_page_form.save(commit=False)
            gallery_instance = Gallery.objects.create(title=new_page_instance.title)
            new_page_instance.gallery = gallery_instance
            new_page_instance.save()

            for form in gallery_formset:
                if form.cleaned_data.get('image'):  # Check if 'image' field is present
                    gallery_image = form.save(commit=False)
                    gallery_image.gallery = gallery_instance
                    gallery_image.save()

            return redirect('success_url')
        else:
            print(new_page_form.errors)
            print(gallery_formset.errors)
    else:
        new_page_form = PagesForm()
        gallery_formset = GalleryImageFormSet(queryset=Gallery.objects.none())
    return render(request, 'customadmin/edit_other_page.html',
                  {'title': 'Редактация страницы', 'name': 'страницы', 'form': new_page_form, 'gallery_formset': gallery_formset})


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

            # Save the formset
            gallery_instances = gallery_formset.save(commit=False)

            # Delete images marked for deletion
            for form in gallery_formset.deleted_forms:
                form.instance.delete()

            # Save changes to the database
            for gallery_instance in gallery_instances:
                gallery_instance.gallery = page_instance.gallery
                gallery_instance.save()

            return redirect('success_url')
        else:
            print(page_form.errors)
            print(gallery_formset.errors)
    else:
        page_form = SellsForm(instance=page_instance)
        gallery_formset = GalleryImageFormSet(queryset=GalleryImage.objects.filter(gallery=page_instance.gallery))

    return render(request, 'customadmin/edit_other_page.html', {'title': 'Редактирование новостей',
                                                            'page_instance': page_instance, 'form': page_form,
                                                            'gallery_formset': gallery_formset})


@login_required
@user_passes_test(is_admin)
def users(request):

    all_users = CustomUser.objects.prefetch_related().all()
    
    context = {
        'title': 'Страница пользователей',
        'users': all_users
    }
    
    return render(request, 'customadmin/users.html', context=context)


@login_required
@user_passes_test(is_admin)
def spam(request):
    files = Spam.objects.prefetch_related().all()
    if request.method == 'POST':
        form = SpamForm(request.POST, request.FILES)
        if form.is_valid():
            selected_file = form.cleaned_data['file_name']
            print(selected_file)# Получаем очищенные данные из формы

            all_users = CustomUser.objects.all()
            recipients = [user.email for user in all_users if user.email]

            send_spam_emails.delay(selected_file, recipients)
            return redirect('success_url')
        else:
            print(form.errors)
            print("Трабл")
    else:
        form = SpamForm()

    context = {
        'title': 'Страница рассылки',
        'files': files,
        'form': form
    }

    return render(request, 'customadmin/spam.html', context=context)


@login_required
@user_passes_test(is_admin)
@csrf_exempt
def save_email_file(request):
    if request.method == 'POST' and request.FILES.get('emailFile'):
        email_file = request.FILES['emailFile']
        # Создаем новый объект модели Spam и сохраняем в базу данных
        spam_object = Spam(file_name=email_file.name, file=email_file)
        spam_object.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False})
