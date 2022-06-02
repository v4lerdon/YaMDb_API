from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Title(models.Model):
    name = models.TextField()


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва',
        help_text='Укажите автора отзыва')
    title = models.ForeignKey(
        Title(),
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение, к которому относится отзыв',
        help_text='Укажите произведение, к которому относятся отзыв')
    text = models.TextField(
        verbose_name='Текст отзыва',
        help_text='Введите текст отзыва')
    score = models.IntegerField(
        verbose_name='Оценка произведения от 1 до 10',
        help_text='Оцените произведение по шкале от 1 до 10',
        validators=[
            MaxValueValidator(10),
            MinValueValidator(1)
        ])
    pub_date = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
    
    class Meta:
        constraints = (
            models.UniqueConstraint(fields=('author', 'title'),
                                    name='unique_review'),)
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:15]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор публикации',
        help_text='Укажите автора публикации')
    review = models.ForeignKey(
        Review(),
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Обзор, к которому относятся комментарий',
        help_text='Укажите обзор, к которому относятся комментарии')
    text = models.TextField(
        verbose_name='Текст комментария',
        help_text='Введите текст комментария')
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:15]