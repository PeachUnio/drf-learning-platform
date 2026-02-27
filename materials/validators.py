from rest_framework.serializers import ValidationError


def validate_youtube_linc(value):
    if "youtube.com" not in value:
        raise ValidationError("Ссылка на сторонние источники. Необходимо использовать ютуб.")