from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:food_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:food_id>/', views.cart_remove,
         name='cart_remove'),
    path(r'healthbutler/login?next=/cart/add/<int:food_id>/$', auth_views.LoginView.as_view(),name='login'),
    path('add/<int:food_id>/healthbutler/login/',auth_views.LoginView.as_view(),name='login')
]