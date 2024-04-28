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
        book_title = request.POST.get('Title')
        book_desc = request.POST.get('Description')
        book_isbn = request.POST.get('isbn')
        book_query = "INSERT INTO Book (Title, ISBN, Description) VALUES %s, %s, %s"
        book_query_data = [book_title, book_isbn, book_desc]
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM book WHERE BookID = %s", [book_id])
            book = dictfetchone(cursor)
        with connection.cursor() as cursor:
            cursor.execute(book_query, book_query_data)
            if cursor.rowcount > 0:
                return JsonResponse({'ResponseMessage' : "Book copy successfully created"}, safe=False)
            else:
                return JsonResponse({'ResponseMessage' : "Book copy creation failed. Please try again."}, safe=False)
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

class BookCopyDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        bookcopy_id = request.GET.get('BookCopyID')
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM bookcopy WHERE BookCopyID = %s", [bookcopy_id])
            bookcopy = dictfetchone(cursor)
        return JsonResponse(bookcopy, safe=False)
    def post(self, request, *args, **kwargs):
        library_id = request.POST.get('LibraryID')
        book_id = request.POST.get('BookID')
        book_condition = request.POST.get('BookCondition')
        query = "INSERT INTO BookCopy (LibraryID, BookID, BookCondition) VALUES %s, %s, %s"
        query_data = [library_id, book_id, book_condition]
        if not library_id or not book_id or not book_condition:
            return JsonResponse({ 'ResponseMessage': "Error"}, safe=False)
        with connection.cursor() as cursor:
            cursor.execute(query, query_data)
            if cursor.rowcount > 0:
                return JsonResponse({'ResponseMessage' : "Book copy successfully created"}, safe=False)
            else:
                return JsonResponse({'ResponseMessage' : "Book copy creation failed. Please try again."}, safe=False)
class MemberBookCopyListView(ListView):
    def get(self, request, *args, **kwargs):
        query = "SELECT mbc.BookCopyID, Title, DueDate FROM MemberBookCopy mbc"
        query += " JOIN BookCopy bc ON bc.BookCopyID = mbc.BookCopyID"
        query += " JOIN Book b ON bc.BookID = b.BookID"
        query_data = []
        member_id = request.GET.get('MemberID')
        if member_id:
            query += " WHERE mbc.MemberID = %s"
            query_data.append(member_id)
        with connection.cursor() as cursor:
            cursor.execute(query, query_data)
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
        query = "SELECT BookID, Title, Authors, SUM(CopiesAvailable) AS CopiesAvailable From BookList"
        query_data = []
        #Get LibraryID(s) from URL parameters and add to query, if present
        library_ids = request.GET.getlist('LibraryID')
        if library_ids:
           query += " WHERE LibraryID IN (%s)" % ', '.join(['%s'] * len(library_ids))
           query_data.extend(library_ids)
        else:
            #No library selected, don't query DB
            return JsonResponse([], safe=False)
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
        query += " GROUP BY BookID, Authors"
        with connection.cursor() as cursor:
            cursor.execute(query, query_data)
            booklists = dictfetchall(cursor)
        return JsonResponse(booklists, safe=False)


class BookDetailDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        query = "SELECT * FROM bookdetail WHERE BookID = %s"
        query_data = [book_id]
        with connection.cursor() as cursor:
            cursor.execute(query, query_data)
            bookdetails = dictfetchone(cursor)
        return JsonResponse(bookdetails, safe=False)

class BookCopyDetailListView(ListView):
    def get(self, request, *args, **kwargs):
        query = "SELECT * FROM bookcopydetail"
        query_data = []
        #Get LibraryID(s) from URL parameters and add to query, if present
        library_ids = request.GET.getlist('LibraryID')
        if library_ids:
           query += " WHERE LibraryID IN (%s)" % ', '.join(['%s'] * len(library_ids))
           query_data.extend(library_ids)
        #Get BookID from URL parameters and add to query, if present
        book_id = request.GET.getlist('BookID')
        if book_id:
            if 'WHERE' in query:
                query += " AND"
            else:
                query += " WHERE"
            query += " BookID = %s"
            query_data.append(book_id)
        with connection.cursor() as cursor:
            cursor.execute(query, query_data)
            bookcopydetails = dictfetchall(cursor)
        return JsonResponse(bookcopydetails, safe=False)

class InsertBookDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        return JsonResponse("", safe=False)
    def post(self, request, *args, **kwargs):
        book_id = request.POST.get('BookID')
        book_condition = request.POST.get('BookCondition')
        library_id = request.POST.get('LibraryID')
        if not book_id:
            #Insert book and fetch ID
            book_title = request.POST.get('Title')
            book_desc = request.POST.get('Description')
            book_isbn = request.POST.get('isbn')
            book_query = "INSERT INTO Book (Title, ISBN, Description) VALUES %s, %s, %s"
            book_query_data = [book_title, book_isbn, book_desc]
            with connection.cursor() as cursor:
                cursor.execute(book_query, book_query_data)
                response = dictfetchone(cursor)
                book_id = response.get('BookID')
            #Check if authors already exist in DB

            #Insert authors and fetch IDs
            book_authors = request.POST.getlist('Author')
            author_query = "INSERT INTO Author (FirstName, LastName, MiddleName) VALUES %s, %s, %s"
        copy_query = "INSERT INTO BookCopy (LibraryID, BookID, BookCondition) VALUES %s, %s, %s"
        copy_query_data = [library_id, book_id, book_condition]
        with connection.cursor() as cursor:
            cursor.execute(copy_query, copy_query_data)
            response = dictfetchone(cursor)
            return JsonResponse(response, safe=False)
               
                


            

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

#Standalone function for insert book with authors
def insert_book_with_authors(title, isbn, description, authors, library_id, book_condition):
    with connection.cursor() as cursor:
        # Insert book
        cursor.execute("INSERT INTO Book (Title, ISBN, Description) VALUES (%s, %s, %s)", [title, isbn, description])
        book_id = cursor.lastrowid

        # Insert or retrieve author IDs
        query_data = []
        for i in range(0, len(authors), 3):
            author_data = authors[i:i+3]
            query_data.extend(author_data)
            query = "INSERT INTO Author (FirstName, LastName, MiddleName) VALUES "
            query += ', '.join(['(%s, %s, %s)'] * (len(author_data) // 3))
            cursor.execute(query, query_data)

        # Insert book copy
        cursor.execute("INSERT INTO BookCopy (LibraryID, BookID, BookCondition) VALUES (%s, %s, %s)", [library_id, book_id, book_condition])

        # Retrieve author IDs
        author_ids = []
        for i in range(0, len(authors), 3):
            author_data = authors[i:i+3]
            cursor.execute("SELECT AuthorID FROM Author WHERE FirstName = %s AND LastName = %s AND MiddleName = %s", author_data)
            author_row = cursor.fetchone()
            if author_row:
                author_ids.append(author_row[0])

    return {"BookID": book_id, "LibraryID": library_id, "BookCondition": book_condition, "AuthorIDs": author_ids}
