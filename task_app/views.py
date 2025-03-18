from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.template import loader
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .models import Task,CustomUser
from .forms import CustomUserCreationForm, CustomUserChangeForm, TaskForm, CommentForm
import datetime


# ユーザー登録
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


# ユーザーログイン
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


# ユーザーログアウト
def user_logout(request):
    logout(request)
    return redirect('login')


# ユーザー一覧
def user_list(request): 
    users = CustomUser.objects.all() 
    max = 20 
    paginator = Paginator(users, max)
    page_number = int(request.GET.get('page', 1)) 
    page_obj = paginator.get_page(page_number) 
    
    params = {
        'title' : '職員一覧' ,
        'users' : page_obj ,
    }
    return render(request, 'task_app/user_list.html', params)


# 自分以外のプロフィール表示
def profile(request, user_id):
    user_data = get_object_or_404(CustomUser, id=user_id)
    params = {
        'title' : 'プロフィール' ,
        'user_data' : user_data ,
        'user_id' : user_id ,
    }
    return render(request,'task_app/profile.html', params)


# 自分のプロフィールを表示
@login_required(login_url='/task_app/login')
def my_profile(request):
    my_data = request.user  # ログインユーザーの情報を取得
    return render(request, 'task_app/my_profile.html', {'my_data': my_data})


# 自分のプロフィール修正
@login_required(login_url='/task_app/login')
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('my_profile')) 
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'task_app/edit_profile.html', {'form': form })


# スケジュール関数
def schedule(request):
    """
    カレンダー画面
    """
    template = loader.get_template("task_app/schedule.html")
    return HttpResponse(template.render())

# タスク作成関数
def create_task(request):
    if request.method == 'POST':
        obj = Task()
        task_form = TaskForm(request.POST, instance=obj)
        task_form.save()
        return redirect(reverse('detail_task',kwargs={'task_id': obj.id}))
    
    params = {
        'title':'業務追加',
        'task_form': TaskForm(),
    }
    
    return render(request, 'task_app/create_task.html', params)

# タスク編集関数
def edit_task(request, task_id):
    obj = get_object_or_404(Task, id=task_id)
    
    if request.method == 'POST':
        task_form = TaskForm(request.POST, instance=obj, initial={'owner': obj.owner})
        
        if task_form.is_valid():
            print("✅ フォームが有効です！")
            task = task_form.save(commit=False)
            
            if task.work_progress == '完了' and not task.completion_date:
                task.completion_date = timezone.now().date()

            task.save()
            return redirect(reverse('detail_task', kwargs={'task_id': task.id}))

        else:
            print("❌ フォームにエラーがあります！")
            print("🔍 フォーム全体のエラー:", task_form.errors)
            print("🔍 フォームの非フィールドエラー:", task_form.non_field_errors())

            # 各フィールドごとのエラーを表示
            for field, errors in task_form.errors.items():
                print(f"❌ フィールド '{field}' のエラー: {errors}")

    else:
        task_form = TaskForm(instance=obj)

    params = {
        'title': '業務編集',
        'task_id': task_id,
        'task_form': task_form,
    }

    return render(request, 'task_app/edit_task.html', params)


# タスク削除
def delete_task(request, task_id):
    task_data = get_object_or_404(Task, id=task_id)
    task_data.delete()
    return redirect(reverse('task_list')) 


# タスク詳細
@login_required(login_url='/task_app/login')
def detail_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    comments = task.cmt_task.all()  # 'cmt_task' は'related_name'
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False) 
            comment.owner_task = task 
            comment.owner_user = request.user 
            comment.save()
            test = 'test'
            return redirect('detail_task', task_id=task.id)
    else:
        form = CommentForm()

    params = {
        'title' : '業務詳細' ,
        'task' : task ,
        'id' : task_id ,
        'comments' : comments ,
        'form' : form ,
    }
    return render(request,'task_app/detail_task.html', params)


# タスク一覧
@login_required(login_url='/task_app/login')
def task_list(request):
    tasks = Task.objects.all() # 全てのタスクを取得
    max = 5 # 1ページあたりの表示数
    paginator = Paginator(tasks, max) # ページネーションでページを取得
    page_number = int(request.GET.get('page', 1))  # デフォルトは 1 ページ目
    page_obj = paginator.get_page(page_number) # get_page(page) を呼ぶと、page目のPageインスタンスを取得します。
    
    params = {
        'title' : '業務一覧' ,
        'tasks' : page_obj ,
    }
    return render(request, 'task_app/task_list.html', params)

# 成果



#render関数...render(request, template_name（描画するテンプレートの名前）, context（テンプレートに渡すデータを含む辞書）