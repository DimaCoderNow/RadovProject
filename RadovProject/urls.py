"""
URL configuration for RadovProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from tabel import views as tabel
from gift_card import views as gift_card

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tabel.show_table, name='tabel'),
    path('card/', gift_card.input_card, name='card'),
    path('show-card/', gift_card.show_card, name='show'),
    path('add-card/', gift_card.add_card, name='add_card'),
    path('login/', gift_card.LoginUser.as_view(), name='login'),
    path('logout/', gift_card.logout_user, name='logout'),
]
handler403 = 'gift_card.views.custom_permission_denied'
