from django.conf.urls import url
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', views.home, name='home'),
    path('upload/', views.upload, name='upload'),
    path('signup/', views.signup, name='signup'),
    path('mypage/', views.mypage, name='mypage'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/like/', views.like, name='like'),
    path('notifications/', views.notifications, name='notifications'),
    path('comment/', views.comment, name='comment'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
]
