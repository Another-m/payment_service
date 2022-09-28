"""Payment_service URL Configuration

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
from rest_framework.routers import DefaultRouter

from Stripe.views import index, basket, payment, OrderViewSet, ItemViewSet, item, success, clear_order

r = DefaultRouter()
r.register('item', ItemViewSet)
r.register('order', OrderViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('index/', index, name='index'),
    path('item/', index, name='item'),
    path('<int:item>', item, name='item'),
    path('item/<int:item>', item, name='item'),
    path('order/', basket, name='order'),
    path('buy/<int:order_id>', payment, name='buy'),
    path('success/', success, name='success'),
    path('clear/', clear_order, name='clear'),
    path('api/', include(r.urls)),
]