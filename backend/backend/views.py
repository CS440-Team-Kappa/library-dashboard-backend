from django.db import connection
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
#from .models import Library, Member, Book, Author, Genre, BookCopy, MemberBookCopy, BookList
from .initialize_db import startup
import json

startup()

#Views which return JSON-formatted data from DB using custom SQL queries
#Currently just a template - NOT functioning as we want them to
class LibraryListView(ListView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM library")
            libraries = dictfetchall(cursor)
        return JsonResponse(libraries, safe=False)

class LibraryDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        library_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM library WHERE LibraryID = %s", [library_id])
            library = dictfetchone(cursor)
        return JsonResponse(library, safe=False)

class MemberListView(ListView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM member")
            members = dictfetchall(cursor)
        return JsonResponse(members, safe=False)

class MemberDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        member_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM member WHERE MemberID = %s", [member_id])
            member = dictfetchone(cursor)
        return JsonResponse(member, safe=False)

class BookListView(ListView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM book")
            books = dictfetchall(cursor)
        return JsonResponse(books, safe=False)

class BookDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM book WHERE BookID = %s", [book_id])
            book = dictfetchone(cursor)
        return JsonResponse(book, safe=False)

class AuthorListView(ListView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM author")
            authors = dictfetchall(cursor)
        return JsonResponse(authors, safe=False)

class AuthorDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        author_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM author WHERE AuthorID = %s", [author_id])
            author = dictfetchone(cursor)
        return JsonResponse(author, safe=False)

class GenreListView(ListView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM genre")
            genres = dictfetchall(cursor)
        return JsonResponse(genres, safe=False)

class GenreDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        genre_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM genre WHERE GenreID = %s", [genre_id])
            genre = dictfetchone(cursor)
        return JsonResponse(genre, safe=False)

class BookCopyListView(ListView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM bookcopy")
            bookcopies = dictfetchall(cursor)
        return JsonResponse(bookcopies, safe=False)

class BookCopyDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        bookcopy_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM bookcopy WHERE BookCopyID = %s", [bookcopy_id])
            bookcopy = dictfetchone(cursor)
        return JsonResponse(bookcopy, safe=False)

class MemberBookCopyListView(ListView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM memberbookcopy")
            memberbookcopies = dictfetchall(cursor)
        return JsonResponse(memberbookcopies, safe=False)

class MemberBookCopyDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        memberbookcopy_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM memberbookcopy WHERE MemberBookCopyID = %s", [memberbookcopy_id])
            memberbookcopy = dictfetchone(cursor)
        return JsonResponse(memberbookcopy, safe=False)

class BookListListView(ListView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booklist")
            booklists = dictfetchall(cursor)
        return JsonResponse(booklists, safe=False)

class BookListDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        booklist_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM booklist WHERE BookListID = %s", [booklist_id])
            booklist = dictfetchone(cursor)
        return JsonResponse(booklist, safe=False)

class BookDetailsDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM bookdetails WHERE BookID = %s", [book_id])
            bookdetails = dictfetchall(cursor)
        #if valid response, convert stringified JSON into JSON
        if bookdetails:
            for book in bookdetails:
                if 'Copies' in book and isinstance(book['Copies'], str):
                    try:
                        book['Copies'] = json.loads(book['Copies'])
                    except json.JSONDecodeError:
                        book['Copies'] = []
        return JsonResponse(bookdetails, safe=False)

#Fetch all rows from cursor as dictionary
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

#Fetch one row from cursor as dictionary
def dictfetchone(cursor):
    columns = [col[0] for col in cursor.description]
    return dict(zip(columns, cursor.fetchone()))

	
