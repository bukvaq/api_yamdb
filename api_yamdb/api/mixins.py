from rest_framework import viewsets, mixins


class CustomViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                    mixins.ListModelMixin, viewsets.GenericViewSet):
    """Кастомный вьюсет для Категорий и для Жанров"""
    pass
