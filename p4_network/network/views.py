from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import User, Post, Profile


# INDEX -----------------------------------------
@login_required
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
@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))


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
        profile = Profile()
        profile.user = user
        profile.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


# ADD -------------------------------------------
@login_required
@csrf_exempt
def addpost(request):
    if request.method == "POST":
        post = request.POST.get('post')
        if len(post) != 0:
            new = Post()
            new.post = post
            new.user = request.user
            new.save()
            return JsonResponse({
                'status': 201,
                'post_id': new.id,
                'username': request.user.username,
                'timestamp': new.timestamp.strftime("%B %d, %Y, %I:%M %p")
                },
                status=201
            )
    return JsonResponse({}, status=400)


# EDIT ------------------------------------------
@login_required
@csrf_exempt
# TODO data de edicao do post
def editpost(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        new = request.POST.get('post')
        try:
            post = Post.objects.get(id=post_id)
            if post.user == request.user:
                post.post = new.strip()
                post.lastEdit = timezone.now()
                post.save()
                return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)
    return JsonResponse({}, status=400)


# LIKE ------------------------------------------
@login_required
@csrf_exempt
def like(request):
    if request.method == "POST":
        post_id = request.POST.get('id')
        is_liked = request.POST.get('is_liked')
        try:
            post = Post.objects.get(id=post_id)
            if is_liked == 'no':
                post.likes.add(request.user)
                is_liked = 'yes'
            elif is_liked == 'yes':
                post.likes.remove(request.user)
                is_liked = 'no'
            post.save()
            return JsonResponse({
                'like_count': post.likes.count(),
                'is_liked': is_liked,
                "status": 201
            })
        except:
            return JsonResponse({
                'error': "Post not found", "status": 404
            })
    return JsonResponse({}, status=400)


# FOLLOW ----------------------------------------
@login_required
@csrf_exempt
def follow(request):
    if request.method == "POST":
        user = request.POST.get('user')
        action = request.POST.get('action')
        if action == 'Follow':
            try:
                user = User.objects.get(username=user)
                profile = Profile.objects.get(user=request.user)
                profile.following.add(user)
                profile.save()
                profile = Profile.objects.get(user=user)
                profile.followers.add(request.user)
                profile.save()
                return JsonResponse({
                    'status': 201,
                    'action': "Unfollow",
                    "follower_count": profile.followers.count()
                    },
                    status=201
                )
            except:
                return JsonResponse({}, status=404)
        else:
            try:
                user = User.objects.get(username=user)
                profile = Profile.objects.get(user=request.user)
                profile.following.remove(user)
                profile.save()
                profile = Profile.objects.get(user=user)
                profile.followers.remove(request.user)
                profile.save()
                return JsonResponse({
                    'status': 201,
                    'action': "Follow",
                    "follower_count": profile.followers.count()
                    },
                    status=201
                )
            except:
                return JsonResponse({}, status=404)
    return JsonResponse({}, status=400)


# FOLLOWING -------------------------------------
@login_required
def following(request):
    following = Profile.objects.get(user=request.user).following.all()
    posts = Post.objects.filter(user__in=following).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    if request.GET.get('page') != None:
        try:
            posts = paginator.page(request.GET.get('page'))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    return render(request, 'network/following.html', {
        'posts': posts
    })


# PROFILE ---------------------------------------
@login_required
def profile(request, username):
    try:
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        users_profile = Profile.objects.get(user=request.user)
    except:
        return render(request, 'network/profile.html', {"error": True})
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    context = {
        'posts': posts,
        "user": user,
        "profile": profile,
        'users_profile': users_profile
    }
    return render(request, 'network/profile.html', {
        'posts': posts,
        'user': user,
        'profile': profile,
        'users_profile': users_profile
    })
