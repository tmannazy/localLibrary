import datetime
import uuid

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from catalog.models import Author, Genre, Language, Book, BookInstance


class AuthorListViewTest(TestCase):
	@classmethod
	def setUpTestData(cls):
		number_of_authors = 13

		for author_id in range(number_of_authors):
			Author.objects.create(
				first_name=f'Hero {author_id}',
				last_name=f'Mum {author_id}',
			)

	def test_view_url_exists_at_desired_location(self):
		response = self.client.get('/catalog/authors/')
		self.assertEqual(response.status_code, 200)

	def test_view_url_accessible_by_name(self):
		response = self.client.get(reverse('authors'))
		self.assertEqual(response.status_code, 200)

	def test_views_uses_correct_templates(self):
		response = self.client.get(reverse('authors'))
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'author_list.html')

	def test_pagination_is_two(self):
		response = self.client.get(reverse('authors'))
		self.assertEqual(response.status_code, 200)
		self.assertTrue('is_paginated' in response.context)
		self.assertTrue(response.context['is_paginated'])
		self.assertEqual(len(response.context['author_list']), 2)

	def test_lists_all_authors(self):
		response = self.client.get(reverse('authors') + '?page=2')
		self.assertEqual(response.status_code, 200)
		self.assertTrue('is_paginated' in response.context)
		self.assertTrue(response.context['is_paginated'] == True)
		self.assertEqual(len(response.context['author_list']), 2)


class LoanedBookInstancesByUserListViewTest(TestCase):
	def setUp(self):
		test_user1 = User.objects.create_user(username='testuser1', password='youAre1stuseR')
		test_user2 = User.objects.create_user(username='testuser2', password='youAre2nduseR')

		test_user1.save()
		test_user2.save()

		# permission = Permission.objects.get(name='Set book as returned')
		# test_user2.user_permissions.add(permission)
		# test_user2.save()

		test_author = Author.objects.create(first_name='Charles', last_name='Agunwoke')
		test_genre = Genre.objects.create(name='Comic')
		test_language = Language.objects.create(name='Igbo')
		test_book = Book.objects.create(
			title='Otu nwa amadi akporo Pita Obi',
			summary='The latest Igbo book',
			isbn='3930CNNV',
			author=test_author,
			language=test_language
		)

		genre_objects_for_book = Genre.objects.all()
		test_book.genre.set(genre_objects_for_book)
		test_book.save()

		number_of_book_copies = 30
		for book_copy in range(number_of_book_copies):
			return_date = timezone.localtime() + datetime.timedelta(days=book_copy % 5)
			the_borrower = test_user1 if book_copy % 2 else test_user2
			status = 'm'
			BookInstance.objects.create(
				book=test_book,
				imprint='Nigeria at 2023',
				due_back=return_date,
				borrower=the_borrower,
				status=status,
			)

	def test_redirect_if_not_logged_in(self):
		response = self.client.get(reverse('my-borrowed'))
		self.assertRedirects(response, '/accounts/login/')

	def test_logged_in_uses_correct_template(self):
		login = self.client.login(username='testuser1', password='youAre1stuseR')
		response = self.client.get(reverse('my-borrowed'))
		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, '/catalog/bookinstance_list_borrowed_user.htm')

	def test_only_borrowed_books_in_list(self):
		login = self.client.login(username='testuser1', password='youAre1stuseR')
		response = self.client.get(reverse('my-borrowed'))
		self.assertEqual(response.status_code, 200)
		self.assertTrue('bookinstance_list' in response.context)
		self.assertEqual(len(response.context['bookinstance_list']), 0)
		books = BookInstance.objects.all()[:10]

		for book in books:
			book.status = 'o'
			book.save()

		response = self.client.get(reverse('my-borrowed'))
		self.assertEqual(str(response.context['user']), 'testuser1')
		self.assertEqual(response.status_code, 200)
		self.assertTrue('bookinstance_list' in response.context)

		for bookitem in response.context['bookinstance_list']:
			self.assertEqual(response.context['user'], bookitem.borrower)
			self.assertEqual(bookitem.status, 'o')






# class RenewBookInstancesViewTest(TestCase):
#
# 		return_date = datetime.date.today() + datetime.timedelta(days=5)
# 		self.test_bookinstance1 = BookInstance.objects.create(
# 			book=test_book,
# 			imprint='The Obidient Movement',
# 			due_back=return_date,
# 			borrower=test_user1,
# 			status='o'
# 		)
#
# 		return_date = datetime.date.today() + datetime.timedelta(days=5)
# 		self.test_bookinstance2 = BookInstance.objects.create(
# 			book=test_book,
# 			imprint='Formidable Are Obidients',
# 			due_back=return_date,
# 			borrower=test_user2,
# 			status='o'
# 		)

	# def test_redirect_if_not_logged_in(self):
	# 	response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
	# 	self.assertEqual(response.status_code, 302)
	# 	self.assertTrue(response.url.startswith('/accounts/login/'))

	# def test_forbidden_if_logged_in_but_not_correct_permission(self):
	# 	login = self.client.login(username='testuser1', password='youAre1stuseR')
	# 	response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
	# 	self.assertEqual(response.status_code, 403)

	# def test_logged_in_with_permission_borrowed_book(self):
	# 	login = self.client.login(username='testuser2', password='youAre2nduseR')
	# 	response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance2.pk}))
	# 	self.assertEqual(response.status_code, 200)

	# def test_logged_in_with_permission_another_users_borrowed_book(self):
	# 	login = self.client.login(username='testuser2', password='youAre2nduseR')
	# 	response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
	# 	self.assertEqual(response.status_code, 200)

	# def test_HTTP404_for_invalid_book_if_logged_in(self):
	# 	test_uid = uuid.uuid4()
	# 	login = self.client.login(username='testuser2', password='youAre2nduseR')
	# 	response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': test_uid}))
	# 	self.assertEqual(response.status_code, 404)

	# def test_uses_correct_template(self):
	# 	login = self.client.login(username='testuser2', password='youAre2nduseR')
	# 	response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
	# 	self.assertEqual(response.status_code, 200)
	# 	self.assertTemplateUsed(response, 'catalog/book_renew_librarian.html')

	# def test_form_renewal_date_initially_has_date_three_weeks_in_future(self):
	# 	login = self.client.login(username='testuser2', password='youAre2nduseR')
	# 	response = self.client.get(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}))
	# 	self.assertEqual(response.status_code, 200)
	# 	date_3_weeks_in_future = datetime.date.today() + datetime.timedelta(weeks=3)
	# 	self.assertEqual(response.context['form'].intial['renewal_date'], date_3_weeks_in_future)

	# def test_redirects_to_all_borrowed_book_list_on_success(self):
	# 	login = self.client.login(username='testuser2', password='youAre2nduseR')
	# 	valid_date_in_future = datetime.date.today() + datetime.timedelta(weeks=2)
	# 	response = self.client.post(reverse('renew-book-librarian', kwargs={'pk': self.test_bookinstance1.pk}),
	# 	                            {'renewal_date': valid_date_in_future})
	# 	self.assertRedirects(response, reverse('loaned'))
