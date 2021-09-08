from django.urls import include, path
from rest_framework import routers

from .views import (
    UserViewSet,
    # TitlesViewSet,
    # CategoriesViewSet,
    # CommentsViewSet,
    # GenresViewSet,
    # ReviewsViewSet
)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet,
                basename='users')
# router.register(r'titles', TitlesViewSet,
#                 basename='titles')
# router.register('categories', CategoriesViewSet,
#                 basename='categories')
# router.register(r'genres', GenresViewSet,
#                 basename='genres')
# router.register(r'titles/(?P<title_id>\d+)/reviews',
#                 ReviewsViewSet, basename='reviews')
# router.register(r'titles/(?P<title_id>\d+)/reviews/'
#                 r'(?P<review_id>\d+)/comments',
#                 CommentsViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(router.urls)),
]
