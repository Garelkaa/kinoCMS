from django import forms

from banner.models import MainBanner
from cinema.models import Cinema, CinemaHall, Movie

from gallery.models import GalleryImage, Gallery
from other.models import News, Promotions, Pages, MainPage, Spam
from users.models import CustomUser


class NewsForm(forms.ModelForm):


    class Meta:
        model = News
        fields = ['title', 'description', 'main_image', 'url_trailer', 'active', 'seo_url', 'seo_title', 'seo_keywords',
                  'description_seo']


class CinemaForm(forms.ModelForm):


    class Meta:
        model = Cinema
        fields = ['title', 'description', 'main_image', 'top_image', 'url_trailer', 'active', 'seo_url', 'seo_title', 'seo_keywords',
                  'description_seo']


class SellsForm(forms.ModelForm):

    class Meta:
        model = Promotions
        fields = ['title', 'description', 'main_image', 'url_trailer', 'active', 'seo_url', 'seo_title', 'seo_keywords',
                  'description_seo']


class CinemaHallForm(forms.ModelForm):

    class Meta:
        model = CinemaHall
        fields = ['number', 'description', 'scheme_image', 'top_image', 'seo_url', 'seo_title', 'seo_keywords',
                  'description_seo']


class FilmsForm(forms.ModelForm):
    type = forms.ChoiceField(choices=Movie.TYPE_CHOICES, widget=forms.RadioSelect, label='Тип')

    class Meta:
        model = Movie
        fields = ['title', 'description', 'main_image', 'url_trailer', 'type', 'seo_url', 'seo_title', 'seo_keywords', 'description_seo']


class MainPageForm(forms.ModelForm):

    class Meta:
        model = MainPage
        fields = ['phone_number', 'seo_text', 'seo_url', 'seo_title', 'seo_keywords', 'description_seo']


class AboutCinemaPageForm(forms.ModelForm):

    class Meta:
        model = Pages
        fields = ['title', 'description', 'main_image', 'active', 'seo_url', 'seo_title', 'seo_keywords',
                  'description_seo']


class BarPageForm(forms.ModelForm):

    class Meta:
        model = Pages
        fields = ['title', 'description', 'main_image', 'active', 'seo_url', 'seo_title', 'seo_keywords',
                  'description_seo']


class VipPageForm(forms.ModelForm):

    class Meta:
        model = Pages
        fields = ['title', 'description', 'main_image', 'active', 'seo_url', 'seo_title', 'seo_keywords',
                  'description_seo']


class AdPageForm(forms.ModelForm):

    class Meta:
        model = Pages
        fields = ['title', 'description', 'main_image', 'active', 'seo_url', 'seo_title', 'seo_keywords',
                  'description_seo']


class ChildPageForm(forms.ModelForm):

    class Meta:
        model = Pages
        fields = ['title', 'description', 'main_image', 'active', 'seo_url', 'seo_title', 'seo_keywords',
                  'description_seo']


class PagesForm(forms.ModelForm):

    class Meta:
        model = Pages
        fields = ['title', 'description', 'main_image', 'active', 'seo_url', 'seo_title', 'seo_keywords',
                  'description_seo']


class SpamForm(forms.ModelForm):

    class Meta:
        model = Spam
        fields = ['file_name']


class MainBannerForm(forms.ModelForm):
    class Meta:
        model = MainBanner
        fields = ['image', 'url', 'text']


MainBannerFormSet = forms.modelformset_factory(
    MainBanner, form=MainBannerForm, extra=0, can_delete=True
)


class GalleryImageForm(forms.ModelForm):
    class Meta:
        model = GalleryImage
        fields = ['image']


GalleryImageFormSet = forms.modelformset_factory(
    GalleryImage, form=GalleryImageForm, extra=0, can_delete=True
)


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'card', 'gender', 'language', 'address',
                  'phoneNumber', 'birthdate', 'city', 'email']

