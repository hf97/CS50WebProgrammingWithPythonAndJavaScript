from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import Category, Listing, User, WatchList, Bid, Comment

# INDEX -----------------------------------------
def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(isActive=True)
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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


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


# CATEGORIES ------------------------------------
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Category.objects.all()
    })

def singleCategory(request, category):
    listings = []
    for listing in Listing.objects.filter(isActive=True):
        if str(listing.category) == (category):
            listings.append(listing)
    return render(request, "auctions/simgleCategory.html", {
        "listings": listings,
        "category": category
    })

# WATCHLIST -------------------------------------
def watchlist(request):
    listings = []
    for list in WatchList.objects.all():
        if request.user == list.user:
            for elem in list.listings.all():
                listings.append(elem)
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

def addWatchlist(request, listingId):
    listingToAdd = Listing.objects.get(id=listingId)
    try:
        w = WatchList.objects.get(user=request.user)
        w.listings.add(listingToAdd)
    except:
        watch = WatchList.objects.create(user=request.user)
        watch.listings.add(listingToAdd)
    return HttpResponseRedirect(reverse("listing", args=[listingId]))

def removeWatchlist(request, listingId):
    listing = Listing.objects.get(id=listingId)
    obj = WatchList.objects.get(user=request.user)
    obj.listings.remove(listing)
    return HttpResponseRedirect(reverse("listing", args=[listingId]))


# CREATE LISTING --------------------------------
class NewListing(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all())

def createListing(request):
    form = NewListing()
    return render(request, "auctions/createListing.html", {
        "form": form
    })


# SAVE LISTING ----------------------------------
def saveListing(request):
    if request.method == "POST":
        Listing.objects.create(name=request.POST.get("name"), description=request.POST.get("description"), startingBid=request.POST.get("startingBid"), image=request.POST.get("image"), user=request.user, category=Category.objects.get(id=request.POST.get("category")))
    # TODO messagem erro
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


# LISTING ---------------------------------------
def listing(request, listingId):
    listing = Listing.objects.get(id=listingId)
    comments = []
    for comment in Comment.objects.all():
        if comment.listing.id == listingId:
            comments.append(comment)
    inWL=False
    if request.user == listing.user:
        isMine=True
    else:
        isMine=False
        try:
            obj = WatchList.objects.get(user=request.user)
            if listing in obj.listings.all():
                inWL = True
            else:
                inWL = False
        except:
            print("No watchlist")
    try:
        currentBid = str(listing.latestBid.price) + "€"
    except:
        currentBid = None
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "inWatchlist": inWL,
        "comments": comments[::-1],
        "isMine": isMine,
        "currentBid": currentBid
    })


# REMOVE LISTING --------------------------------
def removeListing(request, listingId):
    # TODO passar para acabado
    # TODO remover de watchlist
    Listing.objects.filter(id=listingId).delete()
    return HttpResponseRedirect(reverse("index"))


# BID -------------------------------------------
def bid(request, listingId):
    listi = Listing.objects.get(id=listingId)
    newBid = Bid.objects.create(bidder=request.user, listing=listi, price=request.POST.get("bidForm"))
    listi.latestBid = newBid
    listi.save()
    return HttpResponseRedirect(reverse("listing", args=[listingId]))

# COMMENT ---------------------------------------
def comment(request, listingId):
    return render(request, "auctions/comment.html", {
        "listingId": listingId
    })

def addComment(request, listingId):
    listi = Listing.objects.get(id=listingId)
    Comment.objects.create(user=request.user,listing=listi, text=request.POST.get("newComment"))
    return HttpResponseRedirect(reverse("listing", args=[listingId]))