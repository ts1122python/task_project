from django import forms
from .models import CustomUser,Task,Comment
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

# 日本語の月名リスト（1月～12月）
MONTHS_JP = {
    1: "1月", 2: "2月", 3: "3月", 4: "4月", 5: "5月", 6: "6月",
    7: "7月", 8: "8月", 9: "9月", 10: "10月", 11: "11月", 12: "12月"
}


# CustomUserのフォーム
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = "username", "department", "my_goal" # passwordは設定しない
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'department':forms.TextInput(attrs={'class':'form-control'}),
            'my_goal':forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            "username": "名前",
            "department": "所属",
            "my_goal": "個人目標",
        }
        help_texts = {
            "username": "名前は必須です。",
            "department": "所属は必須です。",
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "username", "department", "my_goal" # passwordは設定しない
        



# Taskのフォーム
class TaskForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(), 
        empty_label="担当者を選択",
        label="担当者"
    )    

    class Meta:
        model = Task
        fields = 'owner','title','work','boundary','category','reception_date',\
            'due_date','work_progress','option'
        widgets = {
            'owner':forms.TextInput(attrs={'class':'form-control'}),
            'title':forms.TextInput(attrs={'class':'form-control'}),
            'work':forms.TextInput(attrs={'class':'form-control'}),
            'boundary':forms.RadioSelect(attrs={'class':'form-control'}),
            'category':forms.RadioSelect(attrs={'class':'form-control'}),
            'reception_date':forms.SelectDateWidget(attrs={'class':'form-control'},\
                years=[x for x in range(2020, 2050)],months=MONTHS_JP),
            'due_date':forms.SelectDateWidget(attrs={'class':'form-control'},\
                years=[x for x in range(2020, 2050)],months=MONTHS_JP),
            'work_progress': forms.Select(choices=[('未着手', '未着手'),\
                ('進行中', '進行中'), ('完了', '完了')], attrs={'class': 'form-control'}),
            'option':forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'owner':'担当者',
            'title': '業務名',
            'work': '内容',
            'boundary': '内部/外部',
            'category': 'カテゴリ',
            'reception_date': '受付日',
            'due_date': '期日',
            'work_progress': '進捗',
            'option': '備考',
        }
        help_texts = {
            'owner':'担当者名は必須です。',
            'title': '業務名は必須です。（50字以内）',
            'work': '業務内容を記載してください。（1,000字以内）',
        }

        


# Commentのフォーム