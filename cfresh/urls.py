from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, re_path, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/manager/', include('api.v1.manager.urls')),
    path('api/v1/customer/', include('api.v1.customer.urls')),
    path('', include('web.urls',namespace="web")),
    path('api/v1/franchise/', include('api.v1.franchise.urls')),
    path('manager/', include('managers.urls',namespace="managers")),
    path('franchise/', include('franchise.urls',namespace="franchise")),

]

if settings.DEBUG:
    urlpatterns += (
        static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) +
        static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )

