from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('schedule/', views.schedule, name='schedule'),
    path('create_task/', views.create_task, name='create_task'),
    path('edit_task/', views.edit_task, name='edit_task'),
    path('task_list/', views.task_list, name='task_list'),
    path('detail_task/<int:item.id>', views.detail_task, name='detail_task'),
]

#

#    path('user_list/', user_list, name='user_list'),
#    path('profile/', profile, name='profile'),
#    path('result/', result, name='result'),
#    path('edit_profile/', edit_profile, name='edit_profile'),

# ulrpatterns = [path(アクセスするアドレス,呼び出す処理,名前)]