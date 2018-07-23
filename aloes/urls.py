"""aloes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('admin/doc/', include('django.contrib.admindocs.urls')),
    path('admin/', admin.site.urls),
    path('documents/', include('documents.urls')),
    path('gestion/', include('gestion.urls')),
    path('', views.home, name="home"),
    path('about', views.about, name="about"),
    path('login', views.loginView, name="login"),
    path('profile', views.profile, name="profile"),
    path('logout', views.logoutView, name="logout"),
    path('homeTextEdit', views.homeTextEdit, name="homeTextEdit"),
    path('indexAccounts', views.indexAccounts, name="indexAccounts"),
    path('createUser', views.UserCreate.as_view(), name="createUser"),
    path('editUser/<int:pk>', views.UserEdit.as_view(), name="editUser"),
    path('deleleUser/<int:pk>', views.UserDelete.as_view(), name="deleteUser"),
    path('resetPassword/<int:pk>', views.resetPassword, name="resetPassword"),
    path('adminRights/<int:pk>', views.adminRights, name="adminRights"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
