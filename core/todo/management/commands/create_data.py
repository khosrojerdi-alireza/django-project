from django.core.management.base import BaseCommand
from faker import Faker
from django.contrib.auth.models import User
from todo.models import Task
import random
from datetime import datetime


class Command(BaseCommand):
    help = "Closes the specified poll for voting"

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)
        self.fake = Faker()

    def handle(self, *args, **options):

        user = User.objects.create_user(
            username=self.fake.user_name(), password="Test_08582255"
        )
        user.first_name = self.fake.first_name()
        user.last_name = self.fake.last_name()
        user.email = self.fake.email()
        user.save()


        for _ in range(5):
            task = Task.objects.create(
                title=self.fake.text(max_nb_chars=25),
                complete=random.choice([True, False]),
                user=user,
            )
            task.save()