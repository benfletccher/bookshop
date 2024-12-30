from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from django.db import models

# Course model
class Course(models.Model):
    course_id = models.CharField(max_length=10, primary_key=True)  # Custom Course ID like MA103, PH201
    course_name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.course_name


# Book model
class Book(models.Model):
    isbn = models.CharField(max_length=13, primary_key=True)  # ISBNs are typically 13 characters
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    edition = models.CharField(max_length=50, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"{self.title} by {self.author}"


# Cadet model
class Cadet(AbstractUser):
    cadet_id = models.CharField(max_length=20, primary_key=True)  # Custom Cadet ID entered upon account creation
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)  # Enforce unique email addresses
    company = models.CharField(max_length=50, null=True, blank=True)
    grad_year = models.IntegerField(null=True, blank=True)

    USERNAME_FIELD = 'cadet_id'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Listing model
class Listing(models.Model):
    listing_id = models.AutoField(primary_key=True)  # Auto-incremented ID
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="listings")
    cadet = models.ForeignKey(Cadet, on_delete=models.CASCADE, related_name="listings")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date_of_listing = models.DateField(auto_now_add=True)  # Automatically set the date when created

    def __str__(self):
        return f"Listing of {self.book.title} by {self.cadet.first_name} {self.cadet.last_name}"
