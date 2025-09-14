from django.core.management.base import BaseCommand
from faker import Faker
from hangarinorg.models import Priority, Category, Task, Note, SubTask
from django.utils import timezone

class Command(BaseCommand):
    help = 'Create initial data for the application'

    def handle(self, *args, **kwargs):
        self.create_task(10)
        self.create_note(10)
        self.create_subtask(10)

    def create_task(self, count):
        fake = Faker()

        for _ in range(count):
            Task.objects.create(
                task_title=fake.sentence(nb_words=5),
                task_description=fake.paragraph(nb_sentences=3),
                task_deadline=timezone.make_aware(fake.date_time_this_month()),
                task_status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                task_category=Category.objects.order_by('?').first(),
                task_priority=Priority.objects.order_by('?').first()
            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for task created successfully.'))
        
    def create_note(self, count):
        fake = Faker()

        for _ in range(count):
            Note.objects.create(
                note_content=fake.paragraph(nb_sentences=3),
                note_task=Task.objects.order_by('?').first()
            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for notes created successfully.'))
        
    def create_subtask(self, count):
        fake = Faker()

        for _ in range(count):
            SubTask.objects.create(
                sub_title=fake.sentence(nb_words=5),
                sub_status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                sub_parent_task=Task.objects.order_by('?').first()
            )

        self.stdout.write(self.style.SUCCESS(
            'Initial data for subtask created successfully.'))