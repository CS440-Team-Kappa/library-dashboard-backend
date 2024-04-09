"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from backend import views

#endpoints for requesting data in JSON format
urlpatterns = [
    path('admin/', admin.site.urls),
    path('libraries/', views.LibraryListView.as_view(), name='library-list'),
    path('libraries/<int:pk>/', views.LibraryDetailView.as_view(), name='library-detail'),
    path('members/', views.MemberListView.as_view(), name='member-list'),
    path('members/<int:pk>/', views.MemberDetailView.as_view(), name='member-detail'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre-detail'),
    path('bookcopies/', views.BookCopyListView.as_view(), name='bookcopy-list'),
    path('bookcopies/<int:pk>/', views.BookCopyDetailView.as_view(), name='bookcopy-detail'),
    path('memberbookcopies/', views.MemberBookCopyListView.as_view(), name='memberbookcopy-list'),
    path('memberbookcopies/<int:pk>/', views.MemberBookCopyDetailView.as_view(), name='memberbookcopy-detail'),
    path('booklists/', views.BookListListView.as_view(), name='booklist-list'),
    path('booklists/<int:pk>/', views.BookListDetailView.as_view(), name='booklist-detail'),
]
