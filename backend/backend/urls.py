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
    path('members/', views.MemberDetailView.as_view(), name='member-detail'),
    path('member-login/', views.MemberLoginView.as_view(), name='memberlogin-detail'),
    path('member-library/', views.MemberLibraryView.as_view(), name='memberlibrary-detail'),
    path('get-member-library/', views.GetMemberLibraryView.as_view(), name='getmemberlibrary-detail'),
    path('create-employee/', views.CreateEmployeeLibraryView.as_view(), name='create-employee-detail'),
    path('employees/', views.EmployeesListView.as_view(), name='employees-detail'),
    path('books/', views.BookListView.as_view(), name='book-list'),
    path('book/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='author-list'),
    path('authors/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('genres/', views.GenreListView.as_view(), name='genre-list'),
    path('genres/<int:pk>/', views.GenreDetailView.as_view(), name='genre-detail'),
    path('bookcopies/', views.BookCopyDetailView.as_view(), name='bookcopy-detail'),
    path('memberbookcopies/', views.MemberBookCopyListView.as_view(), name='memberbookcopy-list'),
    path('memberbookcopies/<int:pk>/', views.MemberBookCopyDetailView.as_view(), name='memberbookcopy-detail'),
    path('booklists/', views.BookListListView.as_view(), name='booklist-list'),
    path('bookdetail/', views.BookDetailDetailView.as_view(), name='bookdetail-detail'),
    path('bookcopydetail/', views.BookCopyDetailListView.as_view(), name='bookcopydetail-list'),
    path('removembc/', views.MemberBookCopyRemoveDetailView.as_view(), name='memberbookcopyremove-detail'),
    path('updatebook/', views.UpdateBookDetailView.as_view(), name='updatebook-detail'),
    path('deletebookcopy/', views.DeleteBookCopyDetailView.as_view(), name='deletebookcopy-detail')
    path('updatebook/', views.UpdateBookDetailView.as_view(), name='updatebook-detail')
    path('removembc/', views.MemberBookCopyRemoveDetailView.as_view(), name='memberbookcopyremove-detail'),
    path('checkout-book', views.CheckOutDetailView.as_view(), name='checkout-book')
]
