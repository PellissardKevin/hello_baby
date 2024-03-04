from django.contrib import admin
from django.urls import path, include
from reviews.views import UserViewSet, ImageViewSet, BabyViewSet, PregnancieViewSet
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static


router = DefaultRouter()
router.register(r'user', UserViewSet, basename='User')
router.register(r'image', ImageViewSet, basename='Image')
router.register(r'baby', BabyViewSet, basename='Baby')
router.register(r'pregnancie', PregnancieViewSet, basename='Pregnancie')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth.urls')),
    path('', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)