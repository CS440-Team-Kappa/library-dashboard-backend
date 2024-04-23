from django.db import connection

def member_book_checkout():
    with connection.cursor() as cursor:
              # In progress: Should insert into seperate checkouts table to keep track of values and data
              # Consider using REPLACE to or SELECT?
              cursor.execute("""INSERT INTO checkouts(
                            LibraryID INT UNSIGNED UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
                            Address VARCHAR(256) UNIQUE NOT NULL,
                            LibraryName VARCHAR(256)
                            );""")
              # Want BookCopyID, Library ID, BookID
              # From MemberBookCopy: OutDate, DueDate
              #
              # Below is template for above, need to add and replace parameters and values
              # INSERT INTO checkouts (id, book_id, user_id, checkout_date, return_date)
              # VALUES (1, 1, 1, '2024-04-23', NULL);