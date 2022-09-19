from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Genre(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.title


class Title(models.Model):
    name = models.CharField(max_length=200)
    year = models.DateField()
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
