from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    return render(request, "encyclopedia/entry.html", {
        "entry": entry,
        "entry_body": util.view_entry(entry)
    })


def search(request):
    searched_entry = request.GET['entry_name']

    if not searched_entry:
        return HttpResponseRedirect(reverse("wiki:index"))

    return render(request, "encyclopedia/search.html", {
        "matched_entries": util.search_entries(searched_entry)
    })



def new_entry(request):
    if request.method == "POST":
        entry_title = request.POST['entry_title']
    
        if not entry_title:
            return HttpResponseRedirect(reverse("wiki:index"))
        
        if entry_title in util.list_entries():
            return HttpResponse("Entry already exists")
        
        entry_body = request.POST['entry_body']
        util.save_entry(entry_title, entry_body)

        return HttpResponseRedirect(reverse("wiki:entry", args=[entry_title]))

    return render(request, "encyclopedia/new.html")


def edit_entry(request, entry):
    if request.method == "POST":
        util.save_entry(entry, request.POST['entry_body'])

        return HttpResponseRedirect(reverse("wiki:entry", args=[entry]))

    return render(request, "encyclopedia/edit.html", {
        "entry": entry,
        "entry_body": util.get_entry(entry)
    })


def random_entry(request):
    entry_title = util.random_entry()
    return HttpResponseRedirect(reverse("wiki:entry", args=[entry_title]))