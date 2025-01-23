from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

schema_view = get_schema_view(
    openapi.Info(
        title='TASK API Docs',
        default_version='v1',
    )
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Swagger doc
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='api_docs'),
    
    # URLs for custom apps
    path("api/v1/user/", include("user.urls")),
    path("api/v1/tasks/", include("tasks.urls"))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
