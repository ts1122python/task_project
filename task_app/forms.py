from django import forms
from .models import CustomUser,Task,Comment
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm

# 新規登録のフォーム
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username','department', )

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)


# CustomUserのフォーム


# Taskのフォーム
class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Task
        fields = '__all__'
        #['title','work','boundary','category','reception_date', 'due_date','work_progress','option']
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'work':forms.TextInput(attrs={'class':'form-control'}),
            'boundary':forms.RadioSelect(attrs={'class':'form-control'}),
            'category':forms.RadioSelect(attrs={'class':'form-control'}),
            'reception_date':forms.SelectDateWidget(attrs={'class':'form-control'},\
                years=[x for x in range(2020, 2050)]),
            'due_date':forms.SelectDateWidget(attrs={'class':'form-control'},\
                years=[x for x in range(2020, 2050)]),
            'work_progress': forms.Select(choices=[('未着手', '未着手'),\
                ('進行中', '進行中'), ('完了', '完了')], attrs={'class': 'form-control'}),
            'option':forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'title': '業務名',
            'work': '内容',
            'boundary': '内部/外部',
            'category': 'カテゴリ',
            'reception_date': '受付日',
            'due_date': '期日',
            'work_progress': '進捗',
            'option': '備考',
        }
        


# Commentのフォーム