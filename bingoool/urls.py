"""bingoool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from bingool.urls import router as r1


urlpatterns = [
    # path('api/v1', include(r1.urls, namespace='rest_framework')),
    path('api/v1/', include('bingool.urls_api')),
    path('admin/gest', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path("", include("website.urls")),
    path("accounts/", include("accounts.urls")),
    path("users/", include("users.urls")),
    path("finances/", include("finance.urls")),
    path("bingoool/", include("bingool.urls")),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"), 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
                                                        
admin.site.site_header = "Bingoool"
admin.site.index_title = "Bingool ADMIN"
admin.site.site_title = "Sistema de gerenciamento de Partidas"