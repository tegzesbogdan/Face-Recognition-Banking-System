from django.contrib.auth import authenticate, login, get_user_model
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegisterForm
from .forms import ImageUploadForm, LoginForm
from .models import UserImage
from .face_recon import face_login, face_video


User = get_user_model()

def upload_pic(request, form, username):
    if request.method == 'POST':
        if form.is_valid():
            User = get_user_model()
            user = User.objects.get(username=username)
            avatar = form.cleaned_data.get('profile_photo')
            new_user_profile = UserImage.objects.create(user=user, avatar=avatar)
            new_user_profile.save()


def register_page(request):
    register_form = RegisterForm(request.POST or None)
    photo_upload_form = ImageUploadForm(request.POST, request.FILES)
    context = {
        "register_form": register_form,
        "photo_upload_form": photo_upload_form
    }
    if register_form.is_valid():
        username = register_form.cleaned_data.get("username")
        email = register_form.cleaned_data.get("email")
        password1 = register_form.cleaned_data.get("password1")
        password2 = register_form.cleaned_data.get("password2")
        User.objects.create_user(
            username, email, password1
        )
        upload_pic(request, photo_upload_form, username=username)
        messages.success(request, f'Account created for {username}!')
        return redirect('login')
    return render(request, "users/register.html", context)


def login_page(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                user_id = user.id
                face_video()
                if face_login(UserImage.objects.get(user_id = user_id).avatar.url):
                    login(request, user)
                    return redirect('about')
                else:
                    messages.warning(request, f'Face not recognized for {username}!')
                    return redirect('login')
            else:
                messages.warning(request, f'Wrong username or password!')
                return redirect('login')
    else:
        MyLoginForm = LoginForm()
        return render(request, "users/login.html", {"form": MyLoginForm})