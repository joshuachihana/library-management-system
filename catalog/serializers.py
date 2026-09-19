from rest_framework import serializers

from .models import Author, Book, BookCopy, Category, Publisher


class PublisherSerializer(serializers.ModelSerializer):

    class Meta:
        model = Publisher
        fields = [
            "id",
            "name",
            "email",
            "phone",
            "address",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "description",
        ]

        read_only_fields = [
            "id",
        ]


class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = [
            "id",
            "first_name",
            "last_name",
            "biography",
        ]

        read_only_fields = [
            "id",
        ]


class BookSerializer(serializers.ModelSerializer):

    publisher = serializers.PrimaryKeyRelatedField(
        queryset=Publisher.objects.all(),
        allow_null=True,
        required=False,
    )

    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
    )

    authors = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True,
    )

    class Meta:
        model = Book
        fields = [
            "id",
            "isbn",
            "title",
            "description",
            "publication_year",
            "edition",
            "publisher",
            "category",
            "authors",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
        ]


class BookCopySerializer(serializers.ModelSerializer):

    book = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
    )

    class Meta:
        model = BookCopy
        fields = [
            "id",
            "book",
            "barcode",
            "accession_number",
            "shelf_location",
            "status",
            "condition",
            "acquired_at",
        ]

        read_only_fields = [
            "id",
        ]