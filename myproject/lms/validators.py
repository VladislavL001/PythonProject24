from rest_framework.serializers import ValidationError


class YouTubeValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        url = value.get(self.field)

        if url and "youtube.com" not in url:
            raise ValidationError("Разрешены только ссылки на youtube.com")
