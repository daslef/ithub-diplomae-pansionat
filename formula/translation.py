from modeltranslation.translator import TranslationOptions, register

from formula.models import Room


@register(Room)
class RoomTranslation(TranslationOptions):
    pass
