from django.urls import include, path

from rest_framework import routers

from .views import (
    signup, get_token,
    UserViewSet,
    TitlesViewSet,
    CategoriesViewSet,
    CommentsViewSet,
    GenresViewSet,
    ReviewsViewSet
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet,
                basename='users')
router.register(r'titles', TitlesViewSet,
                basename='titles')
router.register('categories', CategoriesViewSet,
                basename='categories')
router.register(r'genres', GenresViewSet,
                basename='genres')
router.register(r'reviews', ReviewsViewSet,
                basename='reviews')
router.register(r'comments', CommentsViewSet,
                basename='comments')

urlpatterns = [
    path('v1/auth/signup/', signup, name='signup'),
    path('v1/auth/token/', get_token, name='token'),
    path('v1/', include(router.urls)),
]
