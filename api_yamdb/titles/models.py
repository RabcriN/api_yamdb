from django.db import models


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    year = models.DateField()
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name
