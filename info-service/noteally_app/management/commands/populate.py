from django.core.management.base import BaseCommand
from noteally_app.models import StudyArea, University

class Command(BaseCommand):
    def handle(self, **options):

        # Add universities
        with open('noteally_app/management/commands/universities.txt', 'r') as f:
            for line in f:
                university = University(name=line.strip())
                university.save()

        # Add study areas
        with open('noteally_app/management/commands/study_areas.txt', 'r') as f:
            for line in f:
                study_area = StudyArea(name=line.strip())
                study_area.save()
