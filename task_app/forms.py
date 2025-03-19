from django import forms
from .models import CustomUser,Task,Comment
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.forms import UserCreationForm,UserChangeForm

# 日本語の月名リスト（1月～12月）
MONTHS_JP = {
    1: '1月', 2: '2月', 3: '3月', 4: '4月', 5: '5月', 6: '6月',
    7: '7月', 8: '8月', 9: '9月', 10: '10月', 11: '11月', 12: '12月'
}


# CustomUserのフォーム
class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(required=False, disabled=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'department', 'my_goal') # passwordは設定しない
        widgets = {
            'username':forms.TextInput(attrs={'class':'form-control'}),
            'first_name':forms.TextInput(attrs={'class':'form-control'}),
            'last_name':forms.TextInput(attrs={'class':'form-control'}),
            'department':forms.TextInput(attrs={'class':'form-control'}),
            'my_goal':forms.TextInput(attrs={'class':'form-control'}),
        }
        labels = {
            'username': '名前',
            'department': '所属',
            'my_goal': '個人目標',
        }
 
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        first_name = cleaned_data.get('first_name')
        last_name = cleaned_data.get('last_name')

        # first_nameとlast_nameを結合してnameを作成
        if first_name and last_name:
            cleaned_data['name'] = f"{first_name} {last_name}"
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # nameの結合結果をCustomUserのusernameなどにセットする場合
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        if first_name and last_name:
            user.username = f"{first_name} {last_name}"  # 必要に応じて変更

        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = 'username', 'first_name', 'last_name', 'department', 'my_goal' # passwordは設定しない
        



# Taskのフォーム
class TaskForm(forms.ModelForm):
    owner = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(), 
        empty_label="担当者を選択",
        label="担当者",
        widget=forms.Select(attrs={'class': 'form-control', 'style': 'font-size: 14px;'})
    )   
    completion_date = forms.DateField(
        required=False,
        input_formats=['%Y-%m-%d'],  # `YYYY-MM-DD` 形式のみ許可
        label="完了日",
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'style': 'font-size: 14px;'})
    )

    class Meta:
        model = Task
        fields = 'owner','title','work','boundary','category','reception_date',\
            'due_date','work_progress','option'
        widgets = {
            'title':forms.TextInput(attrs={'class':'form-control', 'style': 'font-size: 14px;'}),
            'work':forms.Textarea(attrs={'class':'form-control', 'style': 'font-size: 14px;'}),
            'boundary':forms.RadioSelect(),
            'category':forms.RadioSelect(),
            'reception_date':forms.SelectDateWidget(attrs={'class':'form-control w-auto', 'style': 'font-size: 14px;'},\
                years=[x for x in range(2020, 2050)],months=MONTHS_JP),
            'due_date':forms.SelectDateWidget(attrs={'class':'form-control w-auto', 'style': 'font-size: 14px;'},\
                years=[x for x in range(2020, 2050)],months=MONTHS_JP),
            'work_progress': forms.Select(choices=[('未着手', '未着手'),\
                ('進行中', '進行中'), ('完了', '完了')], attrs={'class': 'form-control w-auto', 'style': 'font-size: 14px;'}),
            'option':forms.Textarea(attrs={'class':'form-control', 'style': 'font-size: 14px;'}),
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

    def clean(self):
        cleaned_data = super().clean()
        work_progress = cleaned_data.get("work_progress")
        completion_date = cleaned_data.get("completion_date")

        # work_progress が完了の場合のみ、completion_date を必須にする
        if work_progress == '完了' and not completion_date:
            self.add_error('completion_date', '完了日を入力してください。')

        # work_progress が完了でない場合、completion_date は空でも良い
        if work_progress != '完了':
            cleaned_data['completion_date'] = None  # 完了日を空に設定

        return cleaned_data



# Commentのフォーム
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = 'comment',
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', \
            'rows': 3, 'placeholder': 'コメントを入力...'})
        }