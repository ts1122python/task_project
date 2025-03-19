from django.urls import path
from . import views


urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('schedule/', views.schedule, name='schedule'),
    path('create_task/', views.create_task, name='create_task'),
    path('edit_task/<int:task_id>/', views.edit_task, name='edit_task'),
    path('delete_task/<int:task_id>/', views.delete_task, name='delete_task'),
    path('detail_task/<int:task_id>/', views.detail_task, name='detail_task'),
    path('task_list/', views.task_list, name='task_list'),
    path('user_list/', views.user_list, name='user_list'),
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),

]


#    path('result/', result, name='result'),

# ulrpatterns = [path(アクセスするアドレス,呼び出す処理,名前)]