import csv

import os

from django.core.management.base import BaseCommand
from django.conf import settings
from reviews.models import (Title, Genre, GenreTitle, Category,
                            Review, Comments, User)


class Command(BaseCommand):
    def handle(self, *args, **options):
        DIR_DATA = os.path.join(settings.BASE_DIR, 'static/data/')

        with open(DIR_DATA + 'users.csv', encoding='utf-8-sig') as csvf:
            reader = csv.reader(csvf)
            next(reader)
            User.objects.all().delete()
            for row in reader:
                print(row)
                users = User.objects.create(id=row[0],
                                            username=row[1],
                                            email=row[2],
                                            role=row[3],
                                            bio=row[4],
                                            first_name=row[5],
                                            last_name=row[6],
                                            )
                users.save()

        with open(DIR_DATA + 'category.csv', encoding='utf-8-sig') as csvf:
            reader = csv.reader(csvf)
            next(reader)
            Category.objects.all().delete()
            for row in reader:
                print(row)
                category = Category.objects.create(id=row[0],
                                                   name=row[1],
                                                   slug=row[2],)
                category.save()

        with open(DIR_DATA + 'comments.csv', encoding='utf-8-sig') as csvf:
            reader = csv.reader(csvf)
            next(reader)
            Comments.objects.all().delete()
            for row in reader:
                print(row)
                author = User.objects.get(id=row[3])
                comment = Comments.objects.create(id=row[0],
                                                  review_id=row[1],
                                                  text=row[2],
                                                  author=author,
                                                  pub_date=row[4],)
                comment.save()

        with open(DIR_DATA + 'genre_title.csv', encoding='utf-8-sig') as csvf:
            reader = csv.reader(csvf)
            next(reader)
            GenreTitle.objects.all().delete()
            for row in reader:
                print(row)
                genre_title = GenreTitle.objects.create(id=row[0],
                                                        title_id=row[1],
                                                        genre_id=row[2],)
                genre_title.save()

        with open(DIR_DATA + 'genre.csv', encoding='utf-8-sig') as csvf:
            reader = csv.reader(csvf)
            next(reader)
            Genre.objects.all().delete()
            for row in reader:
                print(row)
                genre = Genre.objects.create(id=row[0],
                                             name=row[1],
                                             slug=row[2],)
                genre.save()

        with open(DIR_DATA + 'review.csv', encoding='utf-8-sig') as csvf:
            reader = csv.reader(csvf)
            next(reader)
            Review.objects.all().delete()
            for row in reader:
                print(row)
                author = User.objects.get(id=row[3])
                review = Review.objects.create(id=row[0],
                                               title_id=row[1],
                                               text=row[2],
                                               author=author,
                                               score=row[4],
                                               pub_date=row[5]
                                               )
                review.save()

        with open(DIR_DATA + 'titles.csv', encoding='utf-8-sig') as csvf:
            reader = csv.reader(csvf)
            next(reader)
            Title.objects.all().delete()
            for row in reader:
                print(row)
                category = Category.objects.get(id=row[3])
                titles = Title.objects.create(id=row[0],
                                              name=row[1],
                                              year=row[2],
                                              category=category,)
                titles.save()
