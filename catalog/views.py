import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from catalog.forms import RenewBookForm
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
	template_name = 'author_detail.html'


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


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
	book_instance = get_object_or_404(BookInstance, pk=pk)

	if request.method == 'POST':
		form = RenewBookForm(request.POST)
		if form.is_valid():
			book_instance.due_back = form.cleaned_data['renewal_date']
			book_instance.save()
			return HttpResponseRedirect(reverse('loaned'))
	else:
		proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
		form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

	context = {
		'form': form,
		'book_instance': book_instance
	}

	return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(PermissionRequiredMixin, CreateView):
	model = Author
	permission_required = 'catalog.can_create_author'
	fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
	initial = {'date_of_death': '11/06/2020'}


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
	model = Author
	permission_required = 'catalog.can_update_author'
	fields = '__all__'


class AuthorDelete(DeleteView):
	model = Author
	permission_required = 'catalog.can_delete_author'
	success_url = reverse_lazy('authors')


class BookCreate(CreateView):
	model = Book
	fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']


class BookUpdate(UpdateView):
	model = Book
	fields = '__all__'


class BookDelete(DeleteView):
	model = Book
	success_url = reverse_lazy('books')
