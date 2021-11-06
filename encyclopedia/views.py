import re ,random 
from typing import Pattern
from django.core.files.base import ContentFile
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse
from django.core.files.storage import default_storage
from . import util
import markdown


filenames = util.list_entries()
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def get_page(request , title):
    with open(f'entries/{title}.md', 'r') as f:
        text = f.read()
        page = markdown.markdown(text)
    return render(request , "encyclopedia/wiki.html" , {
        "title":title , "page":page })

def get_search(request):
    title=request.GET.get('q')
    if util.get_entry(title)== None:
        patt ='[\w\d]*'+ title.upper()
        possible_entries =[]
        for filename in util.list_entries():
            sth = re.search(patt, filename.upper())
            if sth:
                possible_entries.append(filename)
               
        return render (request , "encyclopedia/search_result.html" , 
        {"title":title , "possible_entries":possible_entries})

    return get_page(request , title)


def get_random_entry(request):
    title = random.choice(util.list_entries())
    return get_page(request , title)

def create_page(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title in util.list_entries():
            return render (request , "encyclopedia/create_page.html" , {
                "error":"error" , 
                "entry":title})
        
        util.save_entry(title , request.POST.get("content"))
        return HttpResponseRedirect (reverse('wiki' , args=[title] ))

    return render(request , "encyclopedia/create_page.html" )

def edit_page (request):
    
    if request.method == "POST":
        title= request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title , content)
        return HttpResponseRedirect (reverse('wiki' , args=[title] ))
    title= request.GET.get('title')
    content = util.get_entry(title)
    return render(request , "encyclopedia/edit.html" , {
        "title":title , "page":content})



