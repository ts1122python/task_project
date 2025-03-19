from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

# カスタムユーザーテーブルを管理
class CustomUser(AbstractUser):
    department = models.CharField(max_length=10,)
    my_goal = models.TextField(max_length=1000)

    groups = models.ManyToManyField(
        Group,
        related_name='task_groups',  
        blank=True,  # グループにユーザーが所属していなくても空のリストにする
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='task_permissions',  
        blank=True,  # 権限がなくても空のリストにする
    )

    def __str__(self):
        return f'{self.username}({self.department})'
    
    class Meta:
        ordering = ('id',)

# タスクテーブルを管理
BOUNDARY_CHOICES = [
    ("外部" , "外部") ,
    ("内部" , "内部") ,
    ]

CATEGORY_CHOICES = [
    ("定例" , "定例") ,
    ("単件" , "単件") ,
    ("長期" , "長期") ,
]

class Task(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, \
        related_name='task_owner') 
    title = models.CharField(max_length=50, blank=False, )
    work =  models.TextField(max_length=1000, blank=True, null=True,)
    boundary = models.CharField(max_length=5, choices=BOUNDARY_CHOICES)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)
    reception_date = models.DateField()
    due_date = models.DateField()
    work_progress = models.CharField(max_length=10, blank=False, )
    completion_date = models.DateField(null=True, blank=True)  # 完了日を追加
    option = models.TextField(max_length=1000, blank=True, null=True,)
    
    def __str__(self):
        return f'No.{self.id}　{self.title}:\
            【範囲】{self.boundary}　【種類】{self.category}　【済】{self.work_progress}'
    
    class Meta:
        ordering = ('id',)


# イベントテーブルを管理
class Event(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    event_name = models.CharField(max_length=200)


# コメントテーブルを管理
class Comment(models.Model):
    owner_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, \
        related_name='cmt_user') 
    owner_task = models.ForeignKey(Task, on_delete=models.CASCADE, \
        related_name='cmt_task') 
    comment = models.TextField(max_length=200,)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'No.{self.id}:{self.comment} by{self.owner_user.username}'
    
    class Meta:
        ordering = ('pub_date',)
