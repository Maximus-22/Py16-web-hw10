from django.urls import path

from . import views


app_name = 'quotes'

urlpatterns = [
    path('', views.main, name = 'root'),
    path('<int:page>', views.main, name = 'root_paginate'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('author/<int:author_id>/edit/', views.edit_author, name='edit_author'),
    path('delete_quote/<int:quote_id>/', views.delete_quote, name='delete_quote'),
]