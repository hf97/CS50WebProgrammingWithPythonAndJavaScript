from encyclopedia.util import save_entry
import markdown2

import random

from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from . import util

# INDEX -----------------------------------------
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

# PAGES -----------------------------------------
def testar(teste):
    if(teste is not None):
        return markdown2.markdown(teste)
    return None

def title(request, title):
    return render(request, "encyclopedia/entry.html", {
        "content": testar(util.get_entry(title)),
        "title": title
    })

# NEW PAGE --------------------------------------
class NewPage(forms.Form):
    name = forms.CharField(label="New Page")
    info = forms.CharField(widget=forms.Textarea)

def new(request):
    if request.method == "POST":
        form = NewPage(request.POST)
        print(form)
        if form.is_valid():
            if util.get_entry(form.cleaned_data["name"]) is None:
                title = form.cleaned_data["name"]
                info = form.cleaned_data["info"]
                text = "# " + title + "\n" + info
                util.save_entry(title, text)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "encyclopedia/new.html", {
                "form": form,
                "message": "Already Exists"
            })
        else:
            return render(request, "encyclopedia/new.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/new.html", {
            "form": NewPage()
        })

# RANDOM PAGE -----------------------------------
def randomPage(request):
    entries = util.list_entries() # list of wikis
    selected_page = random.choice(entries)
    return render(request, "encyclopedia/entry.html", {
        "content": testar(util.get_entry(selected_page)),
        "title": selected_page
    })
 
# SEARCH ----------------------------------------
class searchForm(forms.Form):
    searchQuerie = forms.CharField()

def searchResults(name):
    listSearchResults=[]
    entries = util.list_entries()
    for entry in entries:
        if name.lower() in entry.lower():
            listSearchResults.append(entry)
    return listSearchResults


def search(request):
    if(request.method=="POST"):
        form = searchForm(request.POST)
        if util.get_entry(request.POST.get("q")) is not None:
            title = request.POST.get("q")
            return render(request, "encyclopedia/entry.html", {
                "content": testar(util.get_entry(title)),
                "title": title
            })
        else:
            return render(request, "encyclopedia/search.html", {
            "searchResults": searchResults(request.POST.get("q")),
        })
    else:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })


# EDIT ------------------------------------------
# class NewPage(forms.Form):
#     name = forms.CharField(label="New Page")
#     info = forms.CharField(widget=forms.Textarea)



# def new(request):
#     if request.method == "POST":
#         form = NewPage(request.POST)
#         print(form)
#         if form.is_valid():
#             if util.get_entry(form.cleaned_data["name"]) is None:
#                 title = form.cleaned_data["name"]
#                 info = form.cleaned_data["info"]
#                 text = "# " + title + "\n" + info
#                 util.save_entry(title, text)
#                 return HttpResponseRedirect(reverse("index"))
#             else:
#                 return render(request, "encyclopedia/new.html", {
#                 "form": form,
#                 "message": "Already Exists"
#             })
#         else:
#             return render(request, "encyclopedia/new.html", {
#                 "form": form
#             })
#     else:
#         return render(request, "encyclopedia/new.html", {
#             "form": NewPage()
#         })

