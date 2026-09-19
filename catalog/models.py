from django.db import models


class Publisher(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    biography = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Book(models.Model):
    isbn = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    edition = models.CharField(max_length=50, blank=True)

    publisher = models.ForeignKey(
        Publisher,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="books",
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="books",
    )

    authors = models.ManyToManyField(
        Author,
        related_name="books",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class BookCopy(models.Model):

    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", "Available"
        BORROWED = "BORROWED", "Borrowed"
        RESERVED = "RESERVED", "Reserved"
        LOST = "LOST", "Lost"
        DAMAGED = "DAMAGED", "Damaged"
        MAINTENANCE = "MAINTENANCE", "Maintenance"

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name="copies",
    )

    barcode = models.CharField(max_length=100, unique=True)
    accession_number = models.CharField(max_length=100, unique=True)
    shelf_location = models.CharField(max_length=100)

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.AVAILABLE,
    )

    condition = models.CharField(max_length=100, blank=True)
    acquired_at = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} - {self.barcode}"