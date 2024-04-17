from cinema.models import Cinema, CinemaHall, Movie
from other.models import News, Pages, Promotions
from modeltranslation.translator import register, TranslationOptions


@register(Cinema)
class CinemaTranslationOptions(TranslationOptions):
    fields = ('title', 'description')


@register(CinemaHall)
class CinemaHallTranslationOptions(TranslationOptions):
    fields = ('description',)


@register(Movie)
class MovieTranslation(TranslationOptions):
    fields = ('title', 'description')


@register(News)
class NewsTranslation(TranslationOptions):
    fields = ('title', 'description')


@register(Promotions)
class PromotionsTranslation(TranslationOptions):
    fields = ('title', 'description')


@register(Pages)
class PagesTranslation(TranslationOptions):
    fields = ('title', 'description')
