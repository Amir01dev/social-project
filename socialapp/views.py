from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.core.mail import send_mail
from taggit.models import Tag


# Create your views here.
def log_out(request):
    logout(request)
    return HttpResponse("خارج شدید")


def profile(request):
    return HttpResponse("وارد شدید")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user, files=request.FILES)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'user_form': user_form,
    }
    return render(request, 'registration/edit_user.html', context)


def ticket(request):
    sent = False
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            message = f"{cd['name']}\n{cd['email']}\n{cd['phone']}\n\n{cd['message']}"
            send_mail(cd['subject'], message, 'djangowebsiteperson@gmail.com', ['amir010101developer@gmail.com'], fail_silently=False)
            sent = True
    else:
        form = TicketForm()
    context = {
        'form': form,
        'sent': sent
    }
    return render(request, 'forms/ticket.html', context)


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = Post.objects.filter(tags__in=[tag])
    context = {
        'posts': posts,
        'tag': tag,
    }
    return render(request, "social/post-list.html", context)


@login_required
def create_post(request):
    if request.method == "POST":
        form = CreatePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect("social:post_list")
    else:
        form = CreatePostForm()
    return render(request, "forms/create-post.html", {'form': form})
