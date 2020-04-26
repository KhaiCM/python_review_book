from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required
from .views import (
    BookListView,
    BookHomeView,
    LoginView,
    LogoutView,
    BookDetailView,
    BookCategoryView,
    ListBookByCategory,
    BookSearchView,
    BookMarkView,
    BookAddReviewView,
    BookListMarkView,
    sign_up_view,
    )
app_name = 'books'
urlpatterns = [
    # Book
    path('book-list', login_required(BookListView.as_view()), name='listBook'),
    path('book-detail/<int:book_id>', login_required(BookDetailView.as_view()), name='detailBook'),
    path('', login_required(BookHomeView.as_view()), name='home'),
    path('search', login_required(BookSearchView.as_view()), name='search'),
    # Category
    path('category', login_required(BookCategoryView.as_view()), name='categoryIndex'),
    path('category/<int:id>', login_required(ListBookByCategory.as_view()), name='listBookByCategory'),
    # Comment
    path('add-review/', login_required(BookAddReviewView.as_view()), name='add-review'),
    # Mark
    path('mark', login_required(BookListMarkView.as_view()), name='listMarkBook'),
    path('mark/<int:pk>', login_required(BookMarkView.as_view()), name='mark'),
    # Auth
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/signup/', sign_up_view, name='signup'),
    path('accounts/logout/', views.logout_view, name='logout'),
]
