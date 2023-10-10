import json
from django.core.management.base import BaseCommand
from core.models import Exercises
class Command(BaseCommand):
    help = 'Add exercises to the database from a JSON file'

    def add_arguments(self, parser):
        parser.add_argument('filename', type=str)

    def handle(self, *args, **kwargs):
        filename = kwargs['filename']
        with open(filename) as f:
            exercises = json.load(f)
            for exercise in exercises:
                fields = exercise['fields']
                new_exercise = Exercises(
                    body_part=fields['body_part'],
                    equipment=fields['equipment'],
                    name=fields['name'],
                    description=fields['description'],
                )
                new_exercise.save()
        self.stdout.write(self.style.SUCCESS('Successfully added exercises to the database'))


    # python3 manage.py add_exercises core/fixtures/exercises.json

 