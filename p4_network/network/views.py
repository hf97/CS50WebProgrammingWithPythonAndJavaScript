from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import User, Post, Profile


# INDEX -----------------------------------------
def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    if request.GET.get('page') != None:
        try:
            posts = paginator.page(request.GET.get('page'))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    return render(request, 'network/index.html', {
        'posts': posts
    })


# LOGIN -----------------------------------------
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


# LOGOUT ----------------------------------------
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# REGISTER --------------------------------------
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# ADDPOST ---------------------------------------
@login_required
def addPost(request):
    if request.method == "POST":
        post = request.POST.get('post')
        if len(post) != 0:
            obj = Post()
            obj.post = post
            obj.user = request.user
            obj.save()
            context = {
                'status': 201,
                'postId': obj.id,
                'username': request.user.username,
                'timestamp': obj.timestamp.strftime("%b %d %Y, %I:%M %p")
            }
            return JsonResponse(context, status=201)
    return JsonResponse({}, status=400)


# EDITPOST --------------------------------------
def editPost(request):
    pass


# LIKE ------------------------------------------
def like(request):
    pass


# FOLLOW ----------------------------------------
def follow(request):
    pass


# FOLLOWING -------------------------------------
def following(request):
    pass


# PROFILE ---------------------------------------
def profile(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
    except:
        # TODO error
        return render(request, 'network/profile.html', {
            error
        })
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    if request.GET.get('page') != None:
        try:
            posts = paginator.page(request.GET.get('page'))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    return render(request, 'network/profile.html', {
        'posts': posts,
        'user': user,
        'profile': profile,
    })

