"""csv_generator URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from user.views import home_screen_view, login_user, logout_user
from schema.views import get_schema, create_schema, generate_data, edit_schema, delete_column, download_file,\
    delete_schema


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view, name='home'),
    path('login/', login_user, name='login'),
    path('logout', logout_user, name='logout'),
    path('schema/', get_schema, name='schemas'),
    path('schema/new', create_schema, name='create_schema'),
    path('schema/generate', generate_data, name='generate_data'),
    path('schema/<int:pk>/edit', edit_schema, name='edit_schema'),
    path('schema/<int:schema_pk>/column/<int:column_pk>', delete_column, name='delete_column'),
    path('schema/<int:pk>', delete_schema, name='delete_schema'),
    path('download/<str:schema_name>/', download_file, name='download'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
