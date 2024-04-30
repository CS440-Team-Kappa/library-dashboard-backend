from django.db import connection
from django.db import transaction
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
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
    
class EmployeesListView(ListView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM employees")
            employees = dictfetchall(cursor)
        return JsonResponse(employees, safe=False)
    
class MemberDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        password = request.GET.get('password')
        firstName = request.GET.get('firstName')
        lastName = request.GET.get('lastName')
        phoneNumber = request.GET.get('phoneNumber')
        query = "INSERT INTO MEMBER (Email, Password, FirstName, LastName, PhoneNumber) VALUES (%s, %s, %s, %s, %s)"
        query_data = [email, password, firstName, lastName, phoneNumber]
        query2 = "SELECT * FROM MEMBER WHERE Email = %s"
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(query, query_data)
            with connection.cursor() as cursor:
                cursor.execute(query2, [email])
                user = dictfetchone(cursor)
                return JsonResponse(user, safe=False)

class MemberLoginView(DetailView):
    def get(self, request, *args, **kwargs):
        email = request.GET.get('email')
        query = "SELECT * FROM MEMBER WHERE Email = %s"
        with connection.cursor() as cursor:
            cursor.execute(query, [email])
            user = dictfetchone(cursor)
            if user:
                return JsonResponse(user, safe=False)
            else:
                return JsonResponse({'error': 'User not found'}, status=404)
            
class MemberLibraryView(DetailView):
    def get(self, request, *args, **kwargs):
        member_id = request.GET.get('MemberID')
        query = "INSERT INTO LibraryMember (LibraryID, MemberID) VALUES (%s, %s)"
        query_data = [1, member_id]
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(query, query_data)
                if cursor.rowcount > 0:
                    return JsonResponse({'ResponseMessage' : "User created successfully created"}, safe=False)
                else:
                    return JsonResponse({'ResponseMessage' : "User creation failed. Please try again."}, safe=False)

class CreateEmployeeLibraryView(DetailView):
    def get(self, request, *arges, **kwargs):
        memberid = request.GET.get('memberid')
        ssn = request.GET.get('ssn')
        address = request.GET.get('address')
        role = request.GET.get('role')
        query = 'INSERT INTO Employee (MemberID, SSN, Address, Role) VALUES (%s, %s, %s, %s)'
        query_data = (memberid, ssn, address, role)
        query2 = 'SELECT * FROM Employee where MemberID = %s'
        with transaction.atomic():
            with connection.cursor() as cursor:
                cursor.execute(query, query_data)
        with connection.cursor() as cursor:
            cursor.execute(query2, [memberid])
            employee = dictfetchone(cursor)
            if employee:
                return JsonResponse(employee, safe=False)
            else:
                return JsonResponse({'error': 'User not found'}, status=404)


        



   

class BookListView(ListView):
    def get(self, request, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM book")
            books = dictfetchall(cursor)
        return JsonResponse(books, safe=False)

#Used for Book and BookCopy Insertion with appropriate Author/Genre insertions
class BookDetailView(DetailView):
    def get(self, request, *args, **kwargs):
        #Get data from URL params
        book_title = request.GET.get('Title')
        book_desc = request.GET.get('Description')
        book_isbn = request.GET.get('ISBN')
        book_genre_ids = request.GET.getlist('GenreID')
        author_first_names = request.GET.getlist('AuthorFirstName')
        author_last_names = request.GET.getlist('AuthorLastName')
        book_condition = request.GET.get('BookCondition')
        library_id = request.GET.get('LibraryID')
        book_genre_count = 0

        with transaction.atomic():
            #Insert authors and book, getting IDs back
            author_ids = insert_authors(author_first_names, author_last_names)
            if not author_ids:
                return JsonResponse({'ResponseMessage' : "Error adding book"})
            book_id = insert_book(book_title, book_isbn, book_desc)
            if not book_id:
                return JsonResponse({'ResponseMessage' : "Error adding book"})

            #Insert into BookAuthor and BookGenre tables
            book_author_count = insert_book_authors(book_id, author_ids)
            if book_genre_ids and book_id:
                book_genre_count = insert_book_genres(book_id, book_genre_ids)

        #Ensure operation success
        if book_id and (book_author_count == len(author_ids)) and (book_genre_count == len(book_genre_ids)):
            book_copy_insert = insert_book_copy(book_id, library_id, book_condition)
            if book_copy_insert is not None:
                return JsonResponse({'ResponseMessage' : "Book successfully added"})
        return JsonResponse({'ResponseMessage' : "Error adding book"})
            


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
        book_copy_ids = request.GET.getlist('BookCopyID')
        query = "SELECT BookCopyID, Library.LibraryID, LibraryName, BookCopy.BookID, BookCondition, Title FROM BookCopy JOIN Book ON BookCopy.BookID = Book.BookID JOIN Library ON BookCopy.LibraryID = Library.LibraryID"
        query_data = []
        if book_copy_ids:
            query += " WHERE BookCopyID IN (%s)" % ', '.join(['%s'] * len(book_copy_ids))
            query_data.extend(book_copy_ids)
            with connection.cursor() as cursor:
                cursor.execute(query, query_data)
                book_copies = dictfetchall(cursor)
            return JsonResponse(book_copies, safe=False)
        else:
            return JsonResponse([], safe=False)

class MemberBookCopyListView(ListView):
    def get(self, request, *args, **kwargs):
        query = "SELECT mbc.BookCopyID, Title, OutDate, DueDate FROM MemberBookCopy mbc"
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
        #Get BookID from URL params, adding to query if present
        book_id = request.GET.get('BookID')
        query = "SELECT * FROM bookdetail"
        query_data = []
        if book_id:
            query += " WHERE BookID = %s"
            query_data.append(book_id)

        #Get search string
        search_string = request.GET.get('searchString')

        #Find results with Title like search_string, if present
        if search_string:
            if 'WHERE' in query:
                query += " AND"
            else:
                query += " WHERE"
            query += " (Title LIKE %s)"
            query_data.append(f"%{search_string}%")
        with connection.cursor() as cursor:
            cursor.execute(query, query_data)
            if book_id:
                bookdetails = dictfetchone(cursor)
            else:
                bookdetails = dictfetchall(cursor)
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


def is_author_inserted(first_name, last_name):
    query = "SELECT AuthorID FROM Author WHERE FirstName = %s AND LastName = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, [first_name, last_name])
        author_id = cursor.fetchone()
        if author_id:
            return author_id[0]
        else:
            return None

def insert_authors(first_names, last_names):
    query = "INSERT INTO Author (FirstName, LastName) VALUES"
    select_query = "SELECT AuthorID FROM Author WHERE (FirstName, LastName) IN ("
    query_data = []
    author_ids = []
    for fname, lname in zip(first_names, last_names):
        au_id = is_author_inserted(fname, lname)
        if au_id is None:
            query += " (%s, %s), "
            select_query += " (%s, %s), "
            query_data.extend([fname, lname])
        else:
            author_ids.append(au_id)
    if query_data:
        query = query[:-2]  #remove last comma and space
        select_query = select_query[:-2] + ");"
        with connection.cursor() as cursor:
            cursor.execute(query, query_data)
            #Fetch the inserted AuthorIDs
            cursor.execute(select_query, query_data)
            fetched_ids = [row[0] for row in cursor.fetchall()]
            author_ids.extend(fetched_ids)
    if author_ids:
        return author_ids
    return None

def insert_book(title, isbn, desc):
    query = "INSERT INTO Book (Title, ISBN, Description) VALUES (%s, %s, %s)"
    book_id = is_book_inserted(title, isbn)
    if book_id:
        return book_id
    with connection.cursor() as cursor:
        cursor.execute(query, [title, isbn, desc])
        book_id = cursor.lastrowid
    return book_id

def is_book_inserted(title, isbn):
    query = "SELECT BookID FROM Book WHERE Title = %s AND ISBN = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, [title, isbn])
        book_id = cursor.fetchone()
        if book_id is not None:
            return book_id[0]
        else:
            return None

def is_book_author_inserted(book_id, author_id):
    query = "SELECT AuthorID FROM BookAuthor WHERE BookID = %s AND AuthorID = %s"
    with connection.cursor() as cursor:
        cursor.execute(query, [book_id, author_id])
        author_id = cursor.fetchone()
        if author_id is not None:
            return author_id[0]
        else:
            return None

def insert_book_authors(book_id, author_ids):
    query = "INSERT INTO BookAuthor (AuthorID, BookID) VALUES"
    query_data = []
    rowcount = 0
    for a in author_ids:
        if is_book_author_inserted(book_id, a) is None:
            query += " (%s, %s), "
            query_data.extend([a, book_id])
        else:
            rowcount += 1
    if query_data:
        query = query[:-2] #Remove last comma and space
        with connection.cursor() as cursor:
            cursor.execute(query, query_data)
            return cursor.rowcount + rowcount
    return rowcount

def insert_book_genres(book_id, genre_ids):
    query = "INSERT INTO BookGenre (BookID, GenreID) VALUES"
    query_data = []
    for g in genre_ids:
        query += " (%s, %s), "
        query_data.extend([book_id, g])
    query = query[:-2]
    with connection.cursor() as cursor:
        cursor.execute(query, query_data)
        return cursor.rowcount

def insert_book_copy(book_id, lib_id, condition):
    query = "INSERT INTO BookCopy (BookID, LibraryID, BookCondition) VALUES (%s, %s, %s)"
    if book_id and lib_id and condition:
        with connection.cursor() as cursor:
            cursor.execute(query, [book_id, lib_id, condition])
            return cursor.rowcount
    return None

