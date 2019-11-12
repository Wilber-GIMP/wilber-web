from django.core.management.base import BaseCommand
from subprocess import call

class Command(BaseCommand):
    help = 'Update From GIT'

    def handle(self, *args, **kwargs):
        self.update_from_git()
        self.update_pip_packages()
        self.run_db_migrations()
        
    def update_from_git(self):
        call(['git', 'pull'])

    def update_pip_packages(self):
        call(['pip', 'install', '-r', 'requirements/base.txt'])

    def run_db_migrations(self):
        call(['python', 'manage.py', 'migrate'])