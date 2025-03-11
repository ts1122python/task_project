from django.shortcuts import render,redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .models import Task
from .forms import CustomUserCreationForm,TaskForm


# ユーザー登録関数
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse('profile_admin'))
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts_app/register.html', {'form': form})

# ユーザーログイン関数
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # authenticate関数で認証を試みる
        user = authenticate(request, username=username, password=password)
        
        # 認証に成功した場合、ログインさせる
        if user is not None:
            login(request, user)
            return redirect(reverse('schedule'))
        
    return render(request, 'task_app/login.html')

# スケジュール関数
def schedule(request):
    pass

# タスク作成関数
def create_task(request):
    if request.method == 'POST':
        obj = Task()
        task = TaskForm(request.POST, instance=obj)
        task.save()
        return redirect(reverse('detail_task'))
    
    params = {
        'p_title':'タスク編集',
        'form': TaskForm(),
    }
    
    return render(request, 'task_app/create_task.html', params)

# タスク編集関数
def edit_task(request, num):
    obj = Task.objects.get(id=num) # taskにTaskモデルに存在するid=numのインスタンスを代入
    if request.method == 'POST':
        task = TaskForm(request.POST, instance=obj)
        task.save()
        return redirect(reverse('detail_task'))
    
    params = {
        'title': 'タスク編集' ,
        'id':'num' ,
        'form': TaskForm(instance=obj)
    }
    
    return render(request, 'task_app/edit_task.html', params)

# タスク詳細
def detail_task(request):
    data = Task.objects.all(id=num) # id=numの
    params = {
        'title':'タスク詳細',
        'data':data,
    }
    return render(request,'task_app/detail_task.html', params)

# タスク一覧
#@login_required(login_url='/task_app/login')
def task_list(request): # 初期設定のページは１ページ目
    tasks = Task.objects.all() # 全てのタスクを取得
    max = 5 # 1ページあたりの表示数
    paginator = Paginator(tasks, max) # ページネーションでページを取得
    page_number = request.GET.get('page', 1)  # デフォルトは 1 ページ目
    page_obj = paginator.get_page(page_number) # get_page(page) を呼ぶと、page目のPageインスタンスを取得します。
    
    params = {
        'title' : 'タスク一覧' ,
        'tasks' : page_obj ,
    }
    return render(request, 'task_app/task_list.html', params)


# ユーザー一覧
#@login_required(login_url='/task_app/login')


# プロフィール

# 成果

# プロフィール修正

#render関数...render(request, template_name（描画するテンプレートの名前）, context（テンプレートに渡すデータを含む辞書）