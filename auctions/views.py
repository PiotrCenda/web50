from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Auction, User
from .forms import AuctionForm, CommentForm, BidForm


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all()
    })


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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def new_auction(request):
    if request.method == "POST":
        form = AuctionForm(request.POST)

        if form.is_valid():
            auction = form.save(commit=False)
            auction.owner = request.user
            auction.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/new_auction.html", {
            "form": AuctionForm()
        })


@login_required
def comment_auction(request, auction_id):
    if request.method == "POST" and request.user.is_authenticated:
        comment_form = CommentForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.comment_user = request.user
            auct = Auction.objects.get(id=auction_id)
            comment.auction = auct
            comment.save()
        
    return HttpResponseRedirect(reverse("auction", args=[auction_id]))


def auction(request, auction_id):
    starting_bid = Auction.objects.get(id=auction_id).starting_bid
    bid_error = False
    
    try:
        highest_bid = Auction.objects.get(id=auction_id).auction_bids.order_by('-value').first().value
    except AttributeError:
        highest_bid = 0
    
    price = max(starting_bid, highest_bid)

    if request.method == "POST" and request.user.is_authenticated:
        bid_form = BidForm(request.POST)

        if bid_form.is_valid():
            bid = bid_form.save(commit=False)
            
            if bid.value > price:
                bid.bid_user = request.user
                auct = Auction.objects.get(id=auction_id)
                bid.auction = auct
                bid.save()

                return HttpResponseRedirect(reverse("auction", args=[auction_id]))
            
            else:
                bid_error = True

    on_user_watchlist = False
    user_is_owner = False
    user_won = False
    
    if request.user.is_authenticated:
        if Auction.objects.get(id=auction_id) in User.objects.get(id=request.user.id).watchlist.all():
            on_user_watchlist = True
        
        if User.objects.get(id=request.user.id) == Auction.objects.get(id=auction_id).owner:
            user_is_owner = True
        
        if Auction.objects.get(id=auction_id).auction_bids.order_by('-value').first() is not None:
            if User.objects.get(id=request.user.id) == Auction.objects.get(id=auction_id).auction_bids.order_by('-value').first().bid_user and not Auction.objects.get(id=auction_id).active:
                user_won = True


    return render(request, "auctions/auction.html", {
        "auction": Auction.objects.get(id=auction_id),
        "comments": Auction.objects.get(id=auction_id).comments.all(),
        "price": price,
        "comment_form": CommentForm(),
        "bid_form": BidForm(),
        "bid_error": bid_error,
        "on_user_watchlist": on_user_watchlist,
        "active": Auction.objects.get(id=auction_id).active,
        "user_is_owner": user_is_owner,
        "user_won": user_won
    })


@login_required
def watchlist(request):
    user_watchlist = User.objects.get(id=request.user.id).watchlist.all()

    return render(request, "auctions/watchlist.html", {
        "user_watchlist": user_watchlist
    })


@login_required
def add_watchlist(request, auction_id):
    if request.method == "POST" and request.user.is_authenticated:
        User.objects.get(id=request.user.id).watchlist.add(Auction.objects.get(id=auction_id))
        
    return HttpResponseRedirect(reverse("watchlist"))


@login_required
def remove_watchlist(request, auction_id):
    if request.method == "POST" and request.user.is_authenticated:
        User.objects.get(id=request.user.id).watchlist.remove(Auction.objects.get(id=auction_id))
        
    return HttpResponseRedirect(reverse("watchlist"))


@login_required
def close_auction(request, auction_id):
    if request.method == "POST" and request.user.is_authenticated:
        if User.objects.get(id=request.user.id) == Auction.objects.get(id=auction_id).owner:
            Auction.objects.filter(id=auction_id).update(active=False)
        
    return HttpResponseRedirect(reverse("auction", args=[auction_id]))


def categories(request):
    categories = [category[1] for category in Auction.CATEGORIES]
        
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

    
def show_category(request, category_name):
    category_symbol = [category[0] for category in Auction.CATEGORIES if category[1] == category_name][0]
    auctions = Auction.objects.filter(category=category_symbol)

    return render(request, "auctions/index.html", {
        "auctions": auctions
    })
