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
            cursor.execute("SELECT LibraryID, LibraryName FROM library")
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
        query = "SELECT DISTINCT * FROM booklist"
        query_data = []

        #Get libraryID from URL parameters and add to query, if present
        library_id = self.kwargs.get('libID')
        if library_id is not None:
            query += " WHERE LibraryID = %s"
            query_data.append(library_id)

        #Get search string
        search_string = request.GET.get('searchString')

        #Find results with Title or Author like search_string, if present
        if search_string:
            if 'WHERE' in query:
                query += " AND"
            else:
                query += " WHERE"
            query += " (Authors LIKE %s or Title LIKE %s)"
            query_data.append(f"%{search_string}%")
            query_data.append(f"%{search_string}%")

        with connection.cursor() as cursor:
            cursor.execute(query, query_data)
            booklists = dictfetchall(cursor)
        return JsonResponse(booklists, safe=False)

class BookListAggregateListView(ListView):
    def get(self, request, *args, **kwargs):
        query = "CALL get_libraries_book_list(%s)"
        library_ids = request.GET.getlist('LibraryID')
        if not library_ids:
            return JsonResponse([], safe=False)
        library_ids_str = ','.join(library_ids)
        
        with connection.cursor() as cursor:
            cursor.execute(query, [library_ids_str])
            result = dictfetchall(cursor)
        return JsonResponse(result, safe=False)


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

	
