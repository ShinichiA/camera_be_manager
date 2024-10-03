"""camera URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view
from rest_framework.documentation import include_docs_urls
from .core.urls import urlpatterns as core_urls
from .api.urls import urlpatterns as api_urls
from .accounts.urls import urlpatterns as account_urls
from django.conf import settings
from django.conf.urls.static import static

handler400 = "camera.core.views.handle_400"
handler403 = "camera.core.views.handle_403"
handler404 = "camera.core.views.handle_404"
handler500 = "camera.core.views.handle_500"

urlpatterns = [
    path('', include(core_urls)),
    path('auth/', include(account_urls)),
    path('admin/', admin.site.urls),
    path('api/', include(api_urls)),
    path('swagger-docs', get_swagger_view(title='API LIST')),
    path('docs', include_docs_urls(title='API DOCS')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
