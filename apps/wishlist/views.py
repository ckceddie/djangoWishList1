from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from .models import *


def index(request):    # url(r'^main$', views.main),# url(r'^$', views.index),
    return render(request,"wishlist/index.html")

# ========================= [ Login ]==============================

def login(request):
    if request.method != 'POST':
        return redirect('/')
    valid, response = users.objects.validate_and_login(request.POST)
    if valid == False:
        context = {
            "errors" : response
            }
        return render(request,"wishlist/index.html",context)
    else:
        request.session['id'] = response.id
        request.session['name'] = response.name
        return redirect("/dashboard")

# ========================= [ Register ]==============================

def register(request):
    if request.method != 'POST':
        return redirect('/')
    valid, response = users.objects.validate_and_create_user(request.POST)
    if valid:
        request.session['id'] = response.id
        request.session['name'] = response.name
        return redirect("/dashboard")
    else:
        context = {
            "errors" : response
            }
        return render(request,"wishlist/index.html",context)


# ========================= [ Logout]==============================
def logout(request):
    request.session.clear()
    return redirect('/')

# ========================= [ Go to Add-Item Page]==============================
def create(request):
    if 'id' not in request.session :
        errors=[]
        errors.append("Login session expired , plese login again.")
        context = {
            "errors" : errors,
            }
        return redirect("/",context)

    return render(request,"wishlist/create.html")

# ========================= [ Create / Add Item ]==============================
def additem(request):
    if request.method != 'POST':
        return redirect('/dashboard')
    valid, response = wishlist.objects.validate_and_add_item(request)
    if valid:
        return redirect("/dashboard")
    else:
        context = {
            "errors" : response
            }
        return render(request,"wishlist/create.html",context)
# ========================= [ Add to my wish list ]==============================
def addwish(request):
    if request.method != 'POST':
        return redirect('/dashboard')

    if 'id' not in request.session :
        errors=[]
        errors.append("Login failed , plese try again.")
        context = {
            "errors" : errors,
            }
        return redirect("/",context)
    this_user=users.objects.get(id=request.session['id'])
    print request.POST['itemid']
    addlist = wishlist.objects.get(id=request.POST['itemid'])
    this_user.all_items.add(addlist)
    return redirect("/dashboard")

# ========================= [ Remove my wish item ]==============================
def removewish(request):
    if request.method != 'POST':
        return redirect('/dashboard')

    if 'id' not in request.session :
        errors=[]
        errors.append("Login failed , plese try again.")
        context = {
            "errors" : errors,
            }
        return redirect("/",context)
    this_user=users.objects.get(id=request.session['id'])
    removelist = wishlist.objects.get(id=request.POST['itemid'])
    this_user.all_items.remove(removelist)
    return redirect("/dashboard")

# ========================= [ Delete my item ]==============================
def deletewish(request):
    if request.method != 'POST':
        return redirect('/dashboard')

    if 'id' not in request.session :
        errors=[]
        errors.append("Login failed , plese try again.")
        context = {
            "errors" : errors,
            }
        return redirect("/",context)

    deleteitem = wishlist.objects.get(id=request.POST['itemid'])
    deleteitem.delete()
    return redirect("/dashboard")
# ========================= [ show ]==============================
def item(request,item_id):      # url(r'^wish_items/(?P<item_id>[0-9]+)$', views.item),     # This line has changed!
    if 'id' not in request.session :
        errors=[]
        errors.append("Login failed , plese try again.")
        context = {
            "errors" : errors,
            }
        return redirect("/",context)

    userlist = users.objects.filter(all_items__id=item_id)
    try:
        itemdetail=wishlist.objects.get(id=item_id)
    except:
        return redirect("/dashboard")
    context = {
        "itemdetail" : itemdetail,
        "userlist" :userlist
        }
    return render(request,"wishlist/item.html",context)

# ========================= [ dashboard Page]==============================
def dashboard(request):    # url(r'^dashboard$', views.dashboard)
    if 'id' not in request.session :
        errors=[]
        errors.append("Login failed , plese try again.")
        context = {
            "errors" : errors,
            }
        return redirect("/",context)
    else:
        # my-wish-list = wishlist.objects.filter(all_users__id=request.session['id'])
        MyWishList  = wishlist.objects.filter(all_users__id=request.session['id'])
        OtherWishList = wishlist.objects.all().exclude(all_users__id=request.session['id'])

        UserList=users.objects.all()
        context = {
            "MyWishList" : MyWishList,
            "OtherWishList" : OtherWishList,
            "UserList" : UserList
            }
        return render(request,"wishlist/dashboard.html",context)
