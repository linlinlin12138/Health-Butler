from django.urls import path
from . import views
app_name = 'healthbutler'
urlpatterns = [
    path('food/',views.FoodListView.as_view(), name='subject_list'),
    path('food/<pk>/',
            views.FoodDetailView.as_view(),
            name='food_detail'),
    path('food/<pk>/add/',
            views.CourseEnrollView.as_view(),
            name='course_enroll'),
]


