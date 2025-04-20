from modeltranslation.translator import register, TranslationOptions
from .models import NewsAndEvents, ActivityLog

@register(NewsAndEvents)
class NewsAndEventsTranslationOptions(TranslationOptions):
    fields = ('title', 'summary')
    required_languages = ('en',)  # Make English required, others optional

