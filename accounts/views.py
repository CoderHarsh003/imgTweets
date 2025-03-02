from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm
from django.contrib import messages
from .forms import ImageUploadForm, CommentForm
from .models import UserImage, Comment

def image_detail(request, image_id):
    image = get_object_or_404(UserImage, id=image_id)
    comments = image.comments.all().order_by('-created_at')
    comment_form = CommentForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'like' in request.POST:
                if request.user in image.likes.all():
                    image.likes.remove(request.user)  # Unlike
                else:
                    image.likes.add(request.user)  # Like
            elif 'comment' in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.user = request.user
                    new_comment.image = image
                    new_comment.save()
                    return redirect('image_detail', image_id=image.id)
        else:
            return redirect('login')

    return render(request, 'accounts/image_detail.html', {
        'image': image,
        'comments': comments,
        'comment_form': comment_form,
    })

@login_required
def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            user_image = form.save(commit=False)
            user_image.user = request.user
            user_image.save()
            return redirect('profile')
    else:
        form = ImageUploadForm()
    return render(request, 'accounts/upload.html', {'form': form})

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'accounts/profile.html', {'form': form})

def home_view(request):
    images = UserImage.objects.all().order_by('-uploaded_at')
    return render(request, 'accounts/home.html', {'images': images})

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')