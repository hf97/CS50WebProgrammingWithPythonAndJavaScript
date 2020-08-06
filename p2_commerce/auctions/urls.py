from auctions.views import addWatchlist, saveListing
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("categories", views.categories, name="categories"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("createListing", views.createListing, name="createListing"),
    path("listingsWon", views.listingsWon, name="listingsWon"),
    path("saveListing", views.saveListing, name="saveListing"),
    path("<int:listingId>", views.listing, name="listing"),
    path("<str:category>", views.singleCategory, name="singleCategory"),
    path("<int:listingId>/add", views.addWatchlist, name="addWatchlist"),
    path("<int:listingId>/removeWatchlist", views.removeWatchlist, name="removeWatchlist"),
    path("<int:listingId>/comment", views.comment, name="comment"),
    path("<int:listingId>/addComment", views.addComment, name="addComment"),
    path("<int:listingId>/removeListing", views.removeListing, name="removeListing"),
    path("<int:listingId>/bid", views.bid, name="bid")
]
