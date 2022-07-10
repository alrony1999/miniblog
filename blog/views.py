from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm, ChnagePasswordForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from .models import Post
from django.contrib.auth.models import Group
from django.contrib.auth.forms import PasswordChangeForm


def home(request):
    posts = Post.objects.all()
    return render(request, 'blog/home.html', {'posts': posts})


def about(request):
    return render(request, 'blog/about.html')


def contact(request):
    return render(request, 'blog/contact.html')


def dashboard(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        return render(request, 'blog/dashboard.html', {'posts': posts, 'full_name': full_name, 'groups': gps})
    else:
        return HttpResponseRedirect('/login/')


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')


def user_signup(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = SignUpForm(request.POST)
            if form.is_valid():
                user = form.save()
                group = Group.objects.get(name='Author')
                user.groups.add(group)
                messages.success(
                    request, 'Congratulations !! you have become an author !')
                return HttpResponseRedirect('login')
        else:
            form = SignUpForm()

        return render(request, 'blog/signup.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in successfully !")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})
    else:
        return HttpResponseRedirect('/dashboard/')


def change_password(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = ChnagePasswordForm(user=request.user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)
                messages.success(request, 'Password chnaged successfully !')
                return HttpResponseRedirect('/dashboard/')

        else:
            form = ChnagePasswordForm(user=request.user)
        return render(request, 'blog/changepassword.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                desc = form.cleaned_data['desc']
                pst = Post(title=title, desc=desc)
                pst.save()
                messages.success(request, 'Post added successfully !')
                form = PostForm()
        else:
            form = PostForm()
        return render(request, 'blog/addpost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST, instance=pi)
            if form.is_valid():
                form.save()
                messages.success(request, 'Post Updated successfully !')
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)

        return render(request, 'blog/updatepost.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
            messages.success(request, 'Post Deleted successfully !')
            return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')
