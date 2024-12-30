from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('create_account/', views.create_account, name='create_account'),
    path('login/', views.login_page, name="login"),
    path('home_page/', views.home_page, name="home_page"),
    path('browse_listings', views.browse_listings, name='browse_listings'),
    path('logout', views.logout_view, name="logout"),
    path('browse_books', views.browse_books, name='browse_books'),
    path('listings_per_book/<str:book_isbn>/', views.listings_per_book, name='listings_per_book'),
    path('account_page', views.account_page, name="account_page"),
    path('new_book', views.new_book, name="new_book"),
    path('new_listing', views.new_listing, name='new_listing')
]