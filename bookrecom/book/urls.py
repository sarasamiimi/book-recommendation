from django.urls import path
from .views import recommend_books
from book.views import index

urlpatterns = [

    path('',index,name='index')
]

