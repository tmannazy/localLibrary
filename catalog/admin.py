from django.contrib import admin

# Register your models here.
from catalog.models import Book, BookInstance, Author, Genre, Language

# admin.site.register(Book)
# admin.site.register(BookInstance)
# admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Language)


class BooksInline(admin.TabularInline):
	model = Book


class AuthorAdmin(admin.ModelAdmin):
	list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
	fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
	inlines = [BooksInline]


admin.site.register(Author, AuthorAdmin)


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
	list_display = ('book', 'status', 'borrower', 'due_back', 'id')
	list_filter = ('status', 'due_back')
	fieldsets = (
		('Book Info', {
			'fields': ('book', 'imprint', 'id')
		}),
		('Availability', {
			'fields': ('status', 'due_back', 'borrower')
		})
	)


class BooksInstanceInline(admin.TabularInline):
	model = BookInstance


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'display_genre')
	inlines = [BooksInstanceInline]
