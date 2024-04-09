from django.db import models

#Models for DJango database members

class Library(models.Model):
    LibraryID = models.AutoField(primary_key=True)
    Address = models.CharField(max_length=256, unique=True)
    LibraryName = models.CharField(max_length=256)
    class Meta:
        app_label = 'backend'

class Member(models.Model):
    MemberID = models.AutoField(primary_key=True)
    Email = models.EmailField(unique=True)
    FirstName = models.CharField(max_length=256)
    LastName = models.CharField(max_length=256)
    PhoneNumber = models.CharField(max_length=12)
    class Meta:
        app_label = 'backend'

class LibraryMember(models.Model):
    LibraryID = models.ForeignKey(Library, on_delete=models.CASCADE)
    MemberID = models.ForeignKey(Member, on_delete=models.CASCADE)
    class Meta:
        app_label = 'backend'

class Book(models.Model):
    BookID = models.AutoField(primary_key=True)
    ISBN = models.CharField(max_length=100, unique=True)
    Title = models.CharField(max_length=256)
    Description = models.CharField(max_length=512)
    class Meta:
        app_label = 'backend'

class Employee(models.Model):
    MemberID = models.OneToOneField(Member, on_delete=models.CASCADE, primary_key=True)
    SSN = models.CharField(max_length=9, unique=True)
    Address = models.CharField(max_length=256)
    Role = models.CharField(max_length=256)
    class Meta:
        app_label = 'backend'

class Author(models.Model):
    AuthorID = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=256)
    LastName = models.CharField(max_length=256)
    MiddleName = models.CharField(max_length=256, blank=True, null=True)
    class Meta:
        app_label = 'backend'

class Genre(models.Model):
    GenreID = models.AutoField(primary_key=True)
    GenreName = models.CharField(max_length=256, unique=True)
    class Meta:
        app_label = 'backend'

class BookAuthor(models.Model):
    AuthorID = models.ForeignKey(Author, on_delete=models.CASCADE)
    BookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    class Meta:
        app_label = 'backend'

class BookGenre(models.Model):
    BookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    GenreID = models.ForeignKey(Genre, on_delete=models.CASCADE)
    class Meta:
        app_label = 'backend'

class BookCopy(models.Model):
    BookCopyID = models.AutoField(primary_key=True)
    LibraryID = models.ForeignKey(Library, on_delete=models.CASCADE)
    BookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    BookCondition = models.CharField(max_length=256)
    class Meta:
        app_label = 'backend'

class MemberBookCopy(models.Model):
    MemberID = models.ForeignKey(Member, on_delete=models.RESTRICT)
    BookCopyID = models.ForeignKey(BookCopy, on_delete=models.CASCADE)
    OutDate = models.DateTimeField()
    DueDate = models.DateTimeField()
    class Meta:
        app_label = 'backend'

class BookList(models.Model):
    BookID = models.IntegerField(primary_key=True)
    Title = models.CharField(max_length=256)
    Description = models.CharField(max_length=512)
    Authors = models.CharField(max_length=512)
    CopiesAvailable = models.IntegerField()
    class Meta:
        app_label = 'backend'
