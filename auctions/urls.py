from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("categories/", views.categories, name="categories"),
    path("show_category/<str:category_name>/", views.show_category, name="show_category"),
    path("auction/<int:auction_id>/close/", views.close_auction, name="close_auction"),
    path("auction/<int:auction_id>/comment/", views.comment_auction, name="comment_auction"),
    path("auction/<int:auction_id>/bid/", views.bid_auction, name="bid_auction"),
    path("auction/<int:auction_id>/", views.auction, name="auction"),
    path("auction/new/", views.new_auction, name="new_auction"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("watchlist/<int:auction_id>/add/", views.add_watchlist, name="add_watchlist"),
    path("watchlist/<int:auction_id>/remove/", views.remove_watchlist, name="remove_watchlist")
]
