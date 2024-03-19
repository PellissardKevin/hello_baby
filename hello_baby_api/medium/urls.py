from django.contrib import admin
from django.urls import path, include
from reviews.views import (
    UserViewSet, ImageViewSet, BabyViewSet, PregnancieViewSet, ForumViewSet,
    MessageViewSet, BiberonViewSet, UserModelDeleteAPIView, BabyModelDeleteAPIView,
    PasswordResetAPIView,
)
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='User')
router.register(r'image', ImageViewSet, basename='Image')
router.register(r'baby', BabyViewSet, basename='Baby')
router.register(r'pregnancie', PregnancieViewSet, basename='Pregnancie')
router.register(r'forum', ForumViewSet, basename='Forum')
router.register(r'message', MessageViewSet, basename='Message')
router.register(r'biberon', BiberonViewSet, basename='Biberon')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth.urls')),
    path('userdelete/<pk>', UserModelDeleteAPIView.as_view({'delete': 'destroy'}), name='user-delete'),
    path('babydelete/<pk>', BabyModelDeleteAPIView.as_view({'delete': 'destroy'}), name='baby-delete'),
    path('reset_password/', PasswordResetAPIView.as_view(), name='password_reset'),
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
