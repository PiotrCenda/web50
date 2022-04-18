from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator

from .models import User, Post


def index(request):
    if request.method == "POST" and request.user.is_authenticated:
        post = Post()
        post.title = request.POST['title']
        post.text = request.POST['post_body']
        post.owner = request.user
        post.save()

    return render(request, "network/index.html")


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


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


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
    

def load_posts(request, page): 
    profile = request.GET.get("profile", None)
    
    if profile:
        posts = Post.objects.filter(owner=profile).all()
    else:
        posts = Post.objects.all()
        
    posts = posts.order_by("-timestamp").all()  
    paginator = Paginator(posts, 5)
    page_obj = paginator.get_page(page)  
    
    return JsonResponse({"posts": [post.serialize() for post in page_obj], 
                         "has_previous": page_obj.has_previous(),
                         "has_next": page_obj.has_next(),
                         "current": page}, safe=False)
    

def profile(request, id):
    
    return render(request, "network/profile.html", {
        
    })
