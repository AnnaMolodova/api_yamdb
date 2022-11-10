import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Role:
    USER = 'user'
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    ROLE_CHOICES = [
        (USER, 'user'),
        (ADMIN, 'admin'),
        (MODERATOR, 'moderator')
    ]


class User(AbstractUser):
    """Чтобы определить кастомного пользователя определяем свой менеджер."""

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='Имя'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='email'
    )
    password = models.CharField(
        max_length=200,
        default='password',
        verbose_name='Пароль'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='био'
    )
    confirmation_code = models.CharField(
        max_length=20,
        default='0000',
        verbose_name='Код',
        blank=True,
        null=True
    )
    role = models.CharField(
        max_length=16,
        choices=Role.ROLE_CHOICES,
        default=Role.USER,
        verbose_name='Роль'
    )

    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_moderator(self):
        return self.role == Role.MODERATOR

    @property
    def is_user(self):
        return self.role == Role.USER

    class Meta:
        verbose_name = 'Пользователь'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]


class Category(models.Model):
    name = models.CharField(
        'Название категории',
        max_length=256
    )
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория'


class Genre(models.Model):
    name = models.CharField(
        'Название жанра',
        max_length=256
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'


class GenreTitle(models.Model):
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    title = models.ForeignKey('Title', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title} {self.genre}'


class Title(models.Model):
    name = models.CharField(max_length=256)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='titles',
        verbose_name='Категория'
    )
    genre = models.ManyToManyField(
        'Genre',
        through='GenreTitle',
        related_name='titles',
        verbose_name='Жанр'
    )
    description = models.TextField(
        'Описание',
        blank=True,
        null=True
    )
    year = models.IntegerField(
        verbose_name='Год',
        validators=[
            MinValueValidator(0),
            MaxValueValidator(datetime.datetime.now().year)
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Произведение'


class Review(models.Model):
    SCORE_CHOICES = (
        (1, '1. Ужасно.'),
        (2, '2. Плохо.'),
        (3, '3. Не очень.'),
        (4, '4. Так себе.'),
        (5, '5. Пойдёт.'),
        (6, '6. Неплохо.'),
        (7, '7. Хорошо.'),
        (8, '8. Очень хорошо.'),
        (9, '9. Шикарно.'),
        (10, '10. Великолепно.')
    )
    id = models.AutoField(primary_key=True)
    title = models.ForeignKey(
        Title,
        verbose_name='titles',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='reviews',
    )
    score = models.SmallIntegerField(
        choices=SCORE_CHOICES,
        verbose_name='Оценка пользователем'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания отзыва'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["title", "author"], name="unique_review"
            ),
        ]

    def __str__(self):
        return self.text


class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    review = models.ForeignKey(
        Review,
        verbose_name='Дата публикации',
        related_name='comments',
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата создания комментария',
        auto_now_add=True
    )

    def __str__(self):
        return self.text
