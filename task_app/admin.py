from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser,Task,Comment

# 管理ツールにCustomUser,Task,Commentのモデルを追加
admin.site.register(CustomUser)
admin.site.register(Task)
admin.site.register(Comment)
