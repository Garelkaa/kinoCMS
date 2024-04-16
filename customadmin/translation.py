from cinema.models import Cinema, CinemaHall, Movie
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
