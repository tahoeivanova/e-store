from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from store.api_views import ProductViewSet, UserViewSet


router = routers.DefaultRouter()
router.register('products', ProductViewSet)
router.register('users', UserViewSet)




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('user/', include('user.urls')),
    path('api/v0/', include(router.urls)),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)