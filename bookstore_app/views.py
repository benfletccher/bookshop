from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CreateAccount, Login, NewBook, NewListing
from .models import Listing, Cadet, Book, Course


# Create your views here.
def landing(request):
    if request.user.is_authenticated:
        # Redirect to the home page for logged-in users
        return redirect('home_page')
    else:
        # Render the base.html for unauthenticated users
        return render(request, 'bookstore_app/base.html')

@login_required
def home_page(request):
    cadet = request.user
    context = {"cadet": cadet}
    return render(request, "bookstore_app/home_page.html", context)

def logout_view(request):
    logout(request)
    return redirect("landing")

def create_account(request):
    if request.method == 'POST':
        form = CreateAccount(request.POST)
        if form.is_valid():
            # Create the cadet user
            cadet = form.save()

            # Assign the cadet user to the 'Cadet' group
            cadet_group = Group.objects.get(name='Cadet')
            cadet.groups.add(cadet_group)

            # show a success message
            messages.success(request, 'Account created successfully!')
            return redirect('/login')  # Redirect to the login page after successful account creation
    else:
        form = CreateAccount()

    return render(request, 'bookstore_app/create_account.html', {'form': form})

def login_page(request):
    if request.method == "POST":
        submittedForm = Login(request.POST)
        if submittedForm.is_valid():
            user = authenticate(cadet_id=submittedForm.cleaned_data['cnumber'], password=submittedForm.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "Welcome back!")
                return redirect('/home_page')
            else: 
                # add message "Invalid Username and Password"
                messages.error(request, "Invalid C-Number or Password")
                return redirect("/login")
    newForm = Login()
    context = {'login_form':newForm}
    return render(request, "bookstore_app/login.html", context)

@login_required
def browse_listings(request):
    listings = Listing.objects.select_related('book', 'book__course', 'cadet').order_by("date_of_listing")
    cadet = request.user
    context = {"listings":listings, "cadet":cadet}
    return render(request, "bookstore_app/browse_listings.html", context)

@login_required
def browse_books(request):
    books = Book.objects.select_related('course').order_by('course')
    context = {"books":books}
    return render(request, "bookstore_app/browse_books.html", context)

@login_required
def listings_per_book(request, book_isbn):
    listings = Listing.objects.select_related('book').filter(book__isbn=book_isbn)
    book = Book.objects.get(isbn=book_isbn)
    context = {"Listings": listings, "book":book}
    return render(request, "bookstore_app/listings_per_book.html", context)

@login_required
def account_page(request):
    cadet = request.user
    context = {"cadet":cadet}
    return render(request, "bookstore_app/account_page.html", context)

import re

def is_valid_isbn13(isbn):
    """Validate the given ISBN-13 with hyphens."""
    # Remove hyphens for validation
    isbn = isbn.replace('-', '')
    # Check length and format
    if not re.match(r'^\d{13}$', isbn):
        return False
    # Compute checksum
    total = sum(int(num) * (1 if idx % 2 == 0 else 3) for idx, num in enumerate(isbn[:12]))
    checksum = (10 - (total % 10)) % 10
    return checksum == int(isbn[-1])

@login_required
def new_book(request):
    if request.method == "POST":
        form = NewBook(request.POST)
        if form.is_valid():
            isbn = form.cleaned_data['isbn']
            if not is_valid_isbn13(isbn):
                form.add_error('isbn', 'Invalid ISBN-13 format or checksum.')
            else:
                cadet = request.user
                id = form.cleaned_data['course']
                course = Course.objects.get(course_id=id)
                title=form.cleaned_data['title'],


                new_book = Book(
                    isbn=isbn,
                    title=title,
                    author=form.cleaned_data.get('author', 'Unknown'),
                    edition=form.cleaned_data.get('edition', 'Not Specified'),
                    course=course,
                )
                new_book.save()
                context = {"book_title": title}
            return render(request, 'bookstore_app/success.html', context)
    else:
        form = NewBook()

    context = {"new_book": form}
    return render(request, 'bookstore_app/new_book.html', context)



@login_required
def new_listing(request):
    if request.method == "POST":
        form = NewListing(request.POST)
        if form.is_valid():
            isbn = form.cleaned_data['isbn']
            if not is_valid_isbn13(isbn):
                form.add_error('isbn', 'Invalid ISBN-13 format or checksum.')
            else:
                cadet = request.user
                book = Book.objects.get(isbn=isbn)
                price = form.cleaned_data['price']

                new_listing = Listing(
                    book = book,
                    cadet = cadet,
                    price = price
                )
                new_listing.save()
                context = {"book_title": "a new listing"}
            return render(request, 'bookstore_app/success.html', context)
    else:
        form = NewListing()
    context = {"new_listing": form}
    return render(request, 'bookstore_app/new_listing.html', context)
