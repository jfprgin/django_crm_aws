from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name=''),
    path('register', views.register, name='register'),
    path('my-login', views.my_login, name='my-login'),
    path('user-logout', views.user_logout, name='user-logout'),

    #CRUD
    path('dasboard', views.dashboard, name='dashboard'),
    path('create-record', views.create_record, name='create-record'),
    path('update-record/<str:pk>', views.update_record, name='update-record'),
    path('record/<str:pk>', views.singular_record, name='record'),
    path('delete-record/<str:pk>', views.delete_record, name='delete-record'),
]