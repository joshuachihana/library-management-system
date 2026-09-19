from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Author, Book, BookCopy, Category, Publisher
from .serializers import (
    AuthorSerializer,
    BookCopySerializer,
    BookSerializer,
    CategorySerializer,
    PublisherSerializer,
)


class PublisherListCreateView(APIView):

    def get(self, request):
        publishers = Publisher.objects.all()

        serializer = PublisherSerializer(
            publishers,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = PublisherSerializer(
            data=request.data
        )

        if serializer.is_valid():
            publisher = serializer.save()

            return Response(
                PublisherSerializer(publisher).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class CategoryListCreateView(APIView):

    def get(self, request):
        categories = Category.objects.all()

        serializer = CategorySerializer(
            categories,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(
            data=request.data
        )

        if serializer.is_valid():
            category = serializer.save()

            return Response(
                CategorySerializer(category).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class AuthorListCreateView(APIView):

    def get(self, request):
        authors = Author.objects.all()

        serializer = AuthorSerializer(
            authors,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = AuthorSerializer(
            data=request.data
        )

        if serializer.is_valid():
            author = serializer.save()

            return Response(
                AuthorSerializer(author).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class BookListCreateView(APIView):

    def get(self, request):

        books = (
            Book.objects
            .select_related("publisher", "category")
            .prefetch_related("authors")
            .all()
        )

        serializer = BookSerializer(
            books,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = BookSerializer(
            data=request.data
        )

        if serializer.is_valid():

            book = serializer.save()

            return Response(
                BookSerializer(book).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

class BookCopyListCreateView(APIView):

    def get(self, request):

        book_copies = (
            BookCopy.objects
            .select_related("book")
            .all()
        )

        serializer = BookCopySerializer(
            book_copies,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = BookCopySerializer(
            data=request.data
        )

        if serializer.is_valid():

            book_copy = serializer.save()

            return Response(
                BookCopySerializer(book_copy).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )