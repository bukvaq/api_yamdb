from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework import routers

from .views import (
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
router.register(r'categories', CategoriesViewSet,
                basename='categories')
router.register(r'genres', GenresViewSet,
                basename='genres')
router.register(r'reviews', ReviewsViewSet,
                basename='reviews')
router.register(r'comments', CommentsViewSet,
                basename='comments')

urlpatterns = [
    path('v1/auth/token/', TokenObtainPairView.as_view(), name='token'),
    path('v1/', include(router.urls)),
]
