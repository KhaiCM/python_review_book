from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LogoutView
from django.contrib.auth.forms import UserCreationForm
from .models import Category, Book, Mark, Review
from .forms import LoginForm, SignUpForm, BookSearchForm, AddBookComment
from django.urls import reverse
# Create your views here.


class BookListView(View):
    template_name = 'user/book_list.html'

    def get(self, request, *args, **kwargs):
        books = Book.objects.all()
        return render(request, self.template_name, {'books': books})


class BookDetailView(View):
    template_name = 'user/detail_book.html'

    def get(self, request, *args, **kwargs):
        book_id = kwargs.get('book_id')
        user = request.user
        book = get_object_or_404(Book, pk=book_id)
        review = Review.objects.filter(book_id=book_id)
        categories = Category.objects.all()
        mark = book.mark_set.all().filter(user=request.user).first()
        if mark is None:
            mark = {}
            mark['id'] = 0
        context = {
            'book': book,
            'review': review,
            'mark': mark,
            'categories': categories
        }
        return render(request, self.template_name, context)


class BookCategoryView(View):
    template_name = 'user/category_book.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})


class ListBookByCategory(View):
    template_name = 'user/list_book_by_category.html'

    def get(self, request, *args, **kwargs):
        category_id = kwargs.get('id')
        books = Book.objects.filter(category_id=category_id)
        context = {
            'books': books,
        }
        return render(request, self.template_name, context)


class BookHomeView(View):
    template_name = 'user/home.html'

    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        return render(request, self.template_name, {'categories': categories})


class BookSearchView(View):
    template_name = 'user/book_list.html'
    form = BookSearchForm

    def get(self, request, *args, **kwargs):
        search_form = self.form(request.GET)
        if search_form.is_valid():
            text = search_form.cleaned_data['text']
            books = Book.objects.filter(name__contains=text)
            content = {
                'text': text,
                'books': books,
            }

            return render(request, self.template_name, content)

        return render(request, self.template_name, {'errors': search_form.errors})


class BookAddReviewView(View):
    form = AddBookComment

    def post(self, request, *args, **kwargs):
        kwargs['book_id'] = request.POST['book_id']

        comment_form = self.form(request.POST)
        if comment_form.is_valid():
            user = request.user

            Review.objects.create(
                user=user,
                review=request.POST['comment'],
                book_id=request.POST['book_id']
            )

        return redirect(reverse('books:detailBook', kwargs={'book_id': request.POST['book_id']}))


class BookListMarkView(View):
    template_name = 'user/list_mark.html'

    def get(self, request, *args, **kwargs):
        marks = Mark.objects.filter(user=request.user)
        return render(request, self.template_name, {'marks': marks})


class BookMarkView(View):
    def post(self, request, pk):
        if pk == 0:
            if 'reading' in request.POST:
                book_id = request.POST['reading']
                book = get_object_or_404(Book, pk=book_id)
                status = 1
                favorite = 0
            elif 'read' in request.POST:
                book_id = request.POST['read']
                book = get_object_or_404(Book, pk=book_id)
                status = 2
                favorite = 0,
            else:
                book_id = request.POST['favorite']
                book = get_object_or_404(Book, pk=book_id)
                status = 0
                favorite = 1,
            mark = Mark(
                status=status,
                favorite=favorite,
                book=book,
                user=request.user
            )
            mark.save()
        else:
            mark = Mark.objects.get(pk=pk)
            if 'reading' in request.POST:
                mark.status = 1
            elif 'read' in request.POST:
                mark.status = 2
            elif 'unread' in request.POST:
                mark.status = 0
            elif 'favorite' in request.POST:
                mark.favorite = 1
            else:
                mark.favorite = 0
            mark.save(update_fields=['status', 'favorite'])
        return HttpResponseRedirect(request.POST['current'])


class LoginView(View):
    def get(self, request, *args, **kwargs):
        template_name = 'auth/login.html'
        form = LoginForm()
        content = {'form': form}
        return render(request, template_name, content)

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('/')

        return HttpResponse('Error username or password')


def sign_up_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=password)
        login(request, user)
        return redirect('/')
    return render(request, 'auth/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('books:login'))


class LogoutView(LogoutView):
    template_name = 'auth/login.html'
    extra_context = {'form': LoginForm()}
