from django.contrib import admin
from django.urls import path

from api import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # get request to display the books
    path('books/', views.BookList.as_view()),
    # get request to display the books according to name
    path('book/<str:name>/', views.BookAuthorName.as_view()),

    # get request to display the all pages
    path('pages/', views.Pages.as_view()),
    # get request to display the page according to id
    path('page/<int:book_id>/<int:page_number>/', views.PageId.as_view()),


    # Edit the book for each author
    path('author/post/', views.AuthorView.as_view()),

    #
    path('author/register/', views.RegisterAuthor.as_view()),

    #
    path('author/login/', views.LoginAuthor.as_view()),
    #######

    #
    path('author/addBook/', views.AuthorAddBook.as_view()),

    #
    path('author/addPages/', views.AuthorAddPages.as_view()),

    #
    path('author/editPage/<int:book_id>/<int:page_number>/', views.AuthorEidtPage.as_view()),

    path('logout/', views.LogoutAuthor.as_view()),
    #######
]
"""
{
"email": "ahmed2001@gmail.com",
"password": "ahmed@2001"
}
"""
