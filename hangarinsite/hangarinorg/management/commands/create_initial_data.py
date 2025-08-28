from django.core.management.base import BaseCommand
from faker import Faker
from django.utils import timezone
from hangarinorg.models import Category, Priority, Task, SubTask, Note
import random

class Command(BaseCommand):
    help = 'Create initial data for the web application'
    
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of records to create')
    
    def handle(self, *args, **options):
        count = options.get('count', 10)
        fake = Faker()
        
        
        categories_data = ['Work', 'School', 'Personal', 'Finance', 'Projects']
        for cat_name in categories_data:
            Category.objects.get_or_create(name=cat_name)
        
        
        priorities_data = ['high', 'medium', 'low', 'critical', 'optional']
        for pri_name in priorities_data:
            Priority.objects.get_or_create(name=pri_name)
        
        categories = list(Category.objects.all())
        priorities = list(Priority.objects.all())
        status_options = ['Pending', 'In Progress', 'Completed']
        
        
        for i in range(count):
            Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                status=random.choice(status_options),
                category=random.choice(categories),
                priority=random.choice(priorities),
            )
        
        tasks = list(Task.objects.all())
        
        
        for i in range(count):
            Note.objects.create(
                task=random.choice(tasks),
                content=fake.paragraph(nb_sentences=2),
            )
        
        
        
        try:

            if hasattr(SubTask, 'parent_task'):
                for i in range(count):
                    SubTask.objects.create(
                        parent_task=random.choice(tasks),
                        title=fake.sentence(nb_words=4),
                        status=random.choice(status_options),
                    )
            elif hasattr(SubTask, 'task'):
                for i in range(count):
                    SubTask.objects.create(
                        task=random.choice(tasks),
                        title=fake.sentence(nb_words=4),
                        status=random.choice(status_options),
                    )
            elif hasattr(SubTask, 'main_task'):
                for i in range(count):
                    SubTask.objects.create(
                        main_task=random.choice(tasks),
                        title=fake.sentence(nb_words=4),
                        status=random.choice(status_options),
                    )
            else:
                self.stdout.write(self.style.ERROR('Could not find the correct field name for SubTask relationship'))
                return
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating subtasks: {e}'))
            return
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} tasks, notes, and subtasks!'))