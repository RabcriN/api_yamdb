from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from users.models import User


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
    description = models.TextField()
    category = models.ForeignKey(Category,
                                 null=True,
                                 on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    score = models.IntegerField(
        default=0,
        validators=[
            MaxValueValidator(100),
            MinValueValidator(1)
        ]
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review'),
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='comments'
    )
    text = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments'
    )
    rewiew = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
