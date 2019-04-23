from django.core.management.base import BaseCommand, CommandError
from movie.models import Movie, Tag
import csv

class Command(BaseCommand):
    help = 'Import movies from csv.'

    def add_arguments(self, parser):
        # ./manage.py import_movies --file ./movies.csv
        parser.add_argument(
            '--file',
            action='store_true',
            help='Parse csv with movie info and save into model.'
        )

    def handle(self, *args, **options):
        if options['file']:
            with open(options['file']) as csvfile:
                movies = csv.DictReader(csvfile, delimiter=',')
                for row in movies:
                    id = row['movieId']
                    title = row['title']
                    year = row['year']
                    tags = row['tags'].split('|')
                    movie = Movie.objects.create(id=id, title=title, year=year)
                    if len(tags) != 0: # tags are optional for now
                        for tag in tags:
                            tag = tag.lower()
                            tag_obj = Tag.objects.filter(name=tag)
                            if len(tag_obj) != 0: # tag exist
                                tag.movie.add(movie)
                            else: # tag doesn't exist
                                new_tag = Tag.objects.create(name=tag)
                                new_tag.movie.add(movie)
        else:
            self.stderr.write(self.style.FAIL('need to specify file location.'))
