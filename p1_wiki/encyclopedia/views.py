import markdown2

from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def testar(teste):
    if(teste is not None):
        return markdown2.markdown(teste)
    return None

def title(request, title):
    return render(request, "encyclopedia/entry.html", {
        "content": testar(util.get_entry(title)),
        "title": title
    })