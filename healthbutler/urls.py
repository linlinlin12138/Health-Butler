from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views
from django.urls import re_path as url

urlpatterns = [
    path('healthbutler/login/', auth_views.LoginView.as_view(),name='login'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/healthbutler/dashboard', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('Home', views.home, name='Home'),
    path('food',views.food_list,name='food_list'),
    path(r'^(?P<fcategory_slug>[-\w]+)/$',
        views.food_list,
        name='food_list_by_fcategory'),
    path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$',
        views.food_detail,
        name='food_detail'),
    path(r'cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path('search/', views.post_search, name='post_search'),
    url(r'^health_qa/(?P<id>\d+)$', views.health_qa_detail,name='health_qa_detail'),
    path('health_qa', views.health_qa,name='health_qa'),
    path('health_checkin', views.health_checkin,name='health_checkin'),
    #path('Login', views.login, name='Login'),
    path('register', views.register, name='register'),
    path('read/', views.read, name='read'),
    path('add/', views.add, name='add'),
    path('delete/<int:id>/', views.dele, name='dele'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('useredit/', views.useredit, name='useredit'),
]

