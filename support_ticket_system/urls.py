"""
URL configuration for support_ticket_system project.

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
from rest_framework.routers import SimpleRouter

from support_ticket_system_app import views

router = SimpleRouter()


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ticket/', views.get_ticket_list, name='get_ticket_list'),
    path('ticket/<int:ticket_id>/', views.ticket_details, name='get_ticket'),
    path('ticket/create/', views.create_ticket, name='create_ticket'),
    path('ticket/update/<int:ticket_id>/', views.update_ticket, name='update_ticket'),
]

urlpatterns += router.urls


