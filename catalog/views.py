from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import generic

from catalog.models import Book, BookInstance, Author, Genre


def index(request):
	num_books = Book.objects.all().count()
	num_instances = BookInstance.objects.all().count()
	num_instances_available = BookInstance.objects.filter(status__exact='a').count()
	num_authors = Author.objects.count()
	num_genres = Genre.objects.filter(name__icontains='program').count()
	num_visits = request.session.get('num_visits', 0)
	request.session['num_visits'] = num_visits + 1

	context = {
		'num_books': num_books,
		'num_instances': num_instances,
		'num_instances_available': num_instances_available,
		'num_authors': num_authors,
		'num_genres': num_genres,
		'num_visits': num_visits

	}

	return render(request, 'index.html', context=context)


class BookListView(generic.ListView):
	model = Book
	context_object_name = 'book_list'
	queryset = Book.objects.all()
	template_name = 'book_list.html'
	paginate_by = 2


class BookDetailView(generic.DetailView):
	model = Book
	template_name = 'book_detail.html'


class AuthorListView(generic.ListView):
	model = Author
	context_object_name = 'author_list'
	template_name = 'author_list.html'
	paginate_by = 2
	queryset = Author.objects.all()


class AuthorDetailView(generic.DetailView):
	model = Author
	template_name = 'author-detail.html'


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
	model = BookInstance
	template_name = 'catalog/bookinstance_list_borrowed_user.html'
	paginate_by = 3

	def get_queryset(self):
		return (
			BookInstance.objects.filter(borrower=self.request.user)
				.filter(status__exact='o')
				.order_by('due_back')
		)


class LibraryLoanedBookListView(PermissionRequiredMixin, generic.ListView):
	model = BookInstance
	permission_required = 'catalog.can_mark_returned'
	template_name = "catalog/loaned_book_list.html"
	paginate_by = 3

	def get_queryset(self):
		return (
			BookInstance.objects
				.filter(status__exact='o')
				.order_by('due_back')
		)
