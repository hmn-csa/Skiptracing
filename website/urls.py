from django.urls import path
from . import views

urlpatterns = [
   path('', views.index),
   path('search', views.search),
   path('search/view',views.overview),
   path('customer',views.customer),
   path('graph',views.graph),
   path('geo',views.geo),
   path('score',views.score),
]

