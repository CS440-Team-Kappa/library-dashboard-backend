from django.db import models
from django.utils import timezone
# Import used classes from models python file
from models import Book
from models import Member

class Checkout(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    checkout_date = models.DateField(default=timezone.now)
    return_date = models.DateField(blank=True, null=True)