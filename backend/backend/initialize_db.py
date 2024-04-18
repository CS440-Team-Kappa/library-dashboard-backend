from django.db import connection

def startup():
    with connection.cursor() as cursor:
        cursor.execute("""CREATE TABLE IF NOT EXISTS Library(
                            LibraryID INT UNSIGNED UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
                            Address VARCHAR(256) UNIQUE NOT NULL,
                            LibraryName VARCHAR(256)
                            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Member(
                            MemberID INT UNSIGNED UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
                            Email VARCHAR(256) UNIQUE NOT NULL,
                            FirstName VARCHAR(256) NOT NULL,
                            LastName VARCHAR(256) NOT NULL,
                            PhoneNumber VARCHAR(12)
                            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS LibraryMember(
                            LibraryID INT UNSIGNED NOT NULL,
                            MemberID INT UNSIGNED NOT NULL,
                            PRIMARY KEY(LibraryID, MemberID),
                            FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Book(
                            BookID INT UNSIGNED UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
                            ISBN VARCHAR(100) UNIQUE NOT NULL,
                            Title VARCHAR(256) NOT NULL,
                            Description VARCHAR(512)
                            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Employee(
                            MemberID INT UNSIGNED UNIQUE NOT NULL,
                            SSN CHAR(9) UNIQUE NOT NULL PRIMARY KEY,
                            Address VARCHAR(256) NOT NULL,
                            Role VARCHAR(256) NOT NULL,
                            FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Author(
                            AuthorID INT UNSIGNED UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
                            FirstName VARCHAR(256) NOT NULL,
                            LastName VARCHAR(256) NOT NULL,
                            MiddleName VARCHAR(256)
                            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS Genre(
                            GenreID INT UNSIGNED UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
                            GenreName VARCHAR(256) UNIQUE NOT NULL
                            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS BookAuthor(
                            AuthorID INT UNSIGNED NOT NULL,
                            BookID INT UNSIGNED NOT NULL,
                            PRIMARY KEY(AuthorID, BookID),
                            FOREIGN KEY (AuthorID) REFERENCES Author(AuthorID)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE,
                            FOREIGN KEY (BookID) REFERENCES Book(BookID)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS BookGenre(
                            BookID INT UNSIGNED NOT NULL,
                            GenreID INT UNSIGNED NOT NULL,
                            PRIMARY KEY(BookID, GenreID),
                            FOREIGN KEY (GenreID) REFERENCES Genre(GenreID)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE,
                            FOREIGN KEY (BookID) REFERENCES Book(BookID)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS BookCopy(
                            BookCopyID INT UNSIGNED UNIQUE NOT NULL PRIMARY KEY AUTO_INCREMENT,
                            LibraryID INT UNSIGNED NOT NULL,
                            BookID INT UNSIGNED NOT NULL,
                            BookCondition VARCHAR(256) NOT NULL,
                                FOREIGN KEY (LibraryID) REFERENCES Library(LibraryID)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE,
                            FOREIGN KEY (BookID) REFERENCES Book(BookID)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                            );""")
        cursor.execute("""CREATE TABLE IF NOT EXISTS MemberBookCopy(
                            MemberID INT UNSIGNED NOT NULL,
                            BookCopyID INT UNSIGNED NOT NULL,
                            OutDate DATETIME NOT NULL,
                            DueDate DATETIME NOT NULL,
                            PRIMARY KEY(MemberID, BookCopyID),
                            FOREIGN KEY (MemberID) REFERENCES Member(MemberID)
                                ON UPDATE CASCADE
                                ON DELETE RESTRICT,
                            FOREIGN KEY (BookCopyID) REFERENCES BookCopy(BookCopyID)
                                ON UPDATE CASCADE
                                ON DELETE CASCADE
                            );""")
        cursor.execute("""CREATE OR REPLACE VIEW BookList AS
                            SELECT DISTINCT b.BookID, b.Title,
                            GROUP_CONCAT(DISTINCT CONCAT(a.FirstName, ' ', COALESCE(a.MiddleName, ''), ' ', a.LastName) SEPARATOR ', ') AS Authors,
                            (SELECT COUNT(*) 
                                    FROM BookCopy bc 
                                    WHERE bc.BookID = b.BookID 
                                      AND bc.LibraryID = lb.LibraryID
                                      AND NOT EXISTS (
                                          SELECT 1
                                          FROM MemberBookCopy mbc
                                          WHERE mbc.BookCopyID = bc.BookCopyID
                                      )
                            ) AS CopiesAvailable
                            FROM Book b
                            LEFT JOIN BookAuthor ba ON b.BookID = ba.BookID
                            LEFT JOIN Author a ON ba.AuthorID = a.AuthorID
                            INNER JOIN BookCopy bc ON b.BookID = bc.BookID
                            INNER JOIN Library lb ON bc.LibraryID = lb.LibraryID
                            GROUP BY b.BookID, b.Title, lb.LibraryID;""")
        cursor.execute("""CREATE OR REPLACE VIEW BookDetails AS 
	                        SELECT b.BookID, b.Title, b.Description, b.ISBN,
                            GROUP_CONCAT(DISTINCT CONCAT(a.FirstName, ' ', COALESCE(a.MiddleName, ''), ' ', a.LastName) SEPARATOR ', ') AS Authors,
                            JSON_ARRAYAGG(
                                JSON_OBJECT(
                                    'BookCopyID', bc.BookCopyID, 
                                    'LibraryID', bc.LibraryID, 
                                    'BookCondition', bc.BookCondition, 
                                    'CheckedOut', CASE WHEN mbc.MemberID IS NOT NULL THEN 'Checked Out' ELSE 'Available' END
                                )
                            ) AS Copies
                            FROM Book b
                            INNER JOIN BookAuthor ba ON b.BookID = ba.bookID
                            INNER JOIN Author a ON ba.AuthorID = a.AuthorID
                            INNER JOIN BookCopy bc ON b.BookID = bc.BookID
                            LEFT JOIN MemberBookCopy mbc ON bc.BookCopyID = mbc.BookCopyID
                            GROUP BY b.BookID;""")

