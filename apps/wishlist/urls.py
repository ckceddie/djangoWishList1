from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^main$', views.index),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^register$', views.register),
    url(r'^wish_items/create$', views.create),
    url(r'^wish_items/additem$', views.additem),
    url(r'^wish_items/addwish$', views.addwish),
    url(r'^wish_items/removewish$', views.removewish),
    url(r'^wish_items/deletewish$', views.deletewish),
    url(r'^wish_items/(?P<item_id>[0-9]+)$', views.item),     
    url(r'^dashboard$', views.dashboard)
    ]
