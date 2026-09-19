from django.urls import path

from .views import (
    AuthorListCreateView,
    BookCopyListCreateView,
    BookListCreateView,
    CategoryListCreateView,
    PublisherListCreateView,
)


urlpatterns = [
    path(
        "publishers/",
        PublisherListCreateView.as_view(),
        name="publisher-list-create",
    ),

    path(
        "categories/",
        CategoryListCreateView.as_view(),
        name="category-list-create",
    ),

    path(
        "authors/",
        AuthorListCreateView.as_view(),
        name="author-list-create",
    ),

    path(
        "books/",
        BookListCreateView.as_view(),
        name="book-list-create",
    ),

    path(
        "book-copies/",
        BookCopyListCreateView.as_view(),
        name="book-copy-list-create",
    ),
]