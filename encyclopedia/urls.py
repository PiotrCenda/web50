from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new_entry, name="new_entry"),
    path("random", views.random_entry, name="random"),
    path("search", views.search, name="search"),
    path("<str:entry>", views.entry, name="entry"),
    path("edit/<str:entry>", views.edit_entry, name="edit_entry")
]
