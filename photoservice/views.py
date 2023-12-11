from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import Photo, Category
from .forms import PhotoForm


# Create your views here.
def index(request):
    photos = Photo.objects.all().order_by('-created_at')
    return render(request, 'photo/index.html', {'photos': photos})


def users_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    photos = user.photo_set.all().order_by('-created_at')
    return render(request, 'photo/users_detail.html',
                  {'user': user, 'photos': photos})


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # ユーザインスタンスを保存
            form.save()
            # UserCreationFormから値を取得する
            input_user = form.cleaned_data['username']
            input_password = form.cleaned_data['password1']
            # フォームの入力値で認証できればユーザオブジェクト、出来なければNoneを返す
            new_user = authenticate(username=input_user, password=input_password)
            if new_user is not None:
                # ログインメソッドは認証が出来なくてもログインさせることができる
                login(request, new_user)
                return redirect('photo:users_detail', pk=new_user.pk)
    else:
        form = UserCreationForm()
    return render(request, 'photo/signup.html', {'form': form})


@login_required
def photos_new(request):
    if request.method == 'POST':
        # request.FILESを引数にわたすことで画像を正常にアップロードできる
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            # commit=FalseにすることでDBに保存しないようにする（外部キーのユーザフィールドが決まっていないため）
            photo = form.save(commit=False)
            photo.user = request.user
            photo.save()
            # 完了時のフラッシュメッセージ
            messages.success(request, "投稿が完了しました！")
        return redirect('photo:users_detail', pk=request.user.pk)
    else:
        form = PhotoForm()
    return render(request, 'photo/photos_new.html', {'form': form})


def photos_detail(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    return render(request, 'photo/photos_detail.html', {'photo': photo})


@require_POST
def photos_delete(request, pk):
    photo = get_object_or_404(Photo, pk=pk)
    photo.delete()
    return redirect('photo:users_detail', request.user.id)


def photos_category(request, category):
    # titleがURLの文字列と一致するCategoryインスタンスを取得
    category = Category.objects.get(title=category)
    # 取得したCategoryに属するPhoto一覧を取得
    photos = Photo.objects.filter(category=category).order_by('-created_at')
    return render(request, 'photo/index.html', {'photos': photos, 'category': category})
