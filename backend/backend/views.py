from django.http import JsonResponse
from django.db import connection

#Return all book objects as dictionary
def get_book_list(request):
	library_ID = request.GET.get('LibraryID')

	if library_ID:
		sql_query = "SELECT * FROM Book WHERE LibraryID = %s"
		
		with connection.cursor() as cursor:
			cursor.execute(sql_query, [library_ID])
			books = dictfetchall(cursor)
	else:
		sql_query = "SELECT * FROM Book"
		with connection.cursor() as cursor:
		cursor.execute(sql_query)
		books = dictfetchall(cursor)

	return JsonResponse({'books': books})


#Returns all rows from cursor as dict
def dictfetchall(cursor):
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]
	