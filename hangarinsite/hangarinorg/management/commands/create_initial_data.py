from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from hangarinorg.models import Category, Priority, Task, SubTask, Note
import random

class Command(BaseCommand):
    help = 'Create computer science tasks with subtasks and notes'
    
    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=50, help='Number of tasks to create')
    
    def handle(self, *args, **options):
        count = options.get('count', 50)

        Task.objects.all().delete()
        SubTask.objects.all().delete()
        Note.objects.all().delete()

        work_cat, _ = Category.objects.get_or_create(name='Work')
        school_cat, _ = Category.objects.get_or_create(name='School') 
        personal_cat, _ = Category.objects.get_or_create(name='Personal')
        projects_cat, _ = Category.objects.get_or_create(name='Projects')
        finance_cat, _ = Category.objects.get_or_create(name='Finance')

        high_pri, _ = Priority.objects.get_or_create(name='high')
        medium_pri, _ = Priority.objects.get_or_create(name='medium') 
        low_pri, _ = Priority.objects.get_or_create(name='low')
        critical_pri, _ = Priority.objects.get_or_create(name='critical')
        optional_pri, _ = Priority.objects.get_or_create(name='optional')

        statuses = ['Pending', 'In Progress', 'Completed']

        cs_tasks = [
            ("Complete Python Data Structures Course", "Master lists, dictionaries, and algorithms", school_cat, high_pri),
            ("Build Flask REST API", "Create RESTful endpoints for web application", projects_cat, medium_pri),
            ("Learn Django Authentication", "Implement user login and registration", projects_cat, high_pri),
            ("Practice Algorithm Problems on LeetCode", "Solve 10 medium difficulty problems", school_cat, medium_pri),
            ("Debug Memory Leak in Application", "Identify and fix memory management issues", work_cat, critical_pri),
            ("Learn Git Advanced Techniques", "Master rebasing, cherry-picking, and hooks", personal_cat, medium_pri),
            ("Write Unit Tests for Project", "Achieve 90% test coverage", work_cat, high_pri),
            ("Study Design Patterns", "Learn Singleton, Factory, Observer patterns", school_cat, medium_pri),
            ("Optimize Database Queries", "Reduce query time by 50%", work_cat, high_pri),
            ("Learn React.js Fundamentals", "Complete React tutorial with hooks", personal_cat, medium_pri),
            ("Create Docker Configuration", "Containerize application for deployment", projects_cat, high_pri),
            ("Study System Design Concepts", "Learn load balancing and scaling", school_cat, high_pri),
            ("Implement CI/CD Pipeline", "Set up automated testing and deployment", work_cat, critical_pri),
            ("Learn TypeScript", "Convert JavaScript project to TypeScript", personal_cat, medium_pri),
            ("Practice Competitive Programming", "Participate in coding competition", school_cat, low_pri),
            ("Build Portfolio Website", "Create personal website with projects", projects_cat, high_pri),
            ("Learn CSS Grid and Flexbox", "Master modern CSS layout techniques", personal_cat, medium_pri),
            ("Implement Responsive Design", "Make website mobile-friendly", work_cat, high_pri),
            ("Study Web Security Best Practices", "Learn HTTPS, CORS, and XSS prevention", school_cat, high_pri),
            ("Optimize Website Performance", "Reduce load time under 2 seconds", work_cat, medium_pri),
            ("Learn GraphQL API Development", "Build GraphQL server with Apollo", personal_cat, medium_pri),
            ("Implement PWA Features", "Add offline capability and push notifications", projects_cat, medium_pri),
            ("Study Web Accessibility Guidelines", "Make website WCAG compliant", work_cat, high_pri),
            ("Learn Webpack Configuration", "Set up module bundler for project", personal_cat, low_pri),
            ("Build E-commerce Site", "Create online store with payment processing", projects_cat, high_pri),
            ("Complete Machine Learning Course", "Finish Coursera ML specialization", school_cat, high_pri),
            ("Learn Pandas Library", "Master data manipulation with Python", personal_cat, medium_pri),
            ("Build Data Visualization Dashboard", "Create charts with Matplotlib/Seaborn", projects_cat, medium_pri),
            ("Study Statistics for Data Science", "Learn probability and distributions", school_cat, high_pri),
            ("Practice SQL Queries", "Complete 20 complex SQL exercises", personal_cat, medium_pri),
            ("Learn TensorFlow Basics", "Build simple neural network", school_cat, medium_pri),
            ("Clean and Preprocess Dataset", "Prepare data for machine learning", work_cat, high_pri),
            ("Study Natural Language Processing", "Learn text processing techniques", school_cat, medium_pri),
            ("Build Recommendation System", "Create movie or product recommender", projects_cat, high_pri),
            ("Learn Data Scraping with BeautifulSoup", "Extract data from websites", personal_cat, low_pri),
            ("Learn AWS Services", "Get familiar with EC2, S3, and Lambda", personal_cat, high_pri),
            ("Set Up Linux Server", "Configure Ubuntu server for deployment", projects_cat, medium_pri),
            ("Study Kubernetes Fundamentals", "Learn container orchestration", school_cat, high_pri),
            ("Implement Monitoring System", "Set up logging and performance monitoring", work_cat, medium_pri),
            ("Learn Ansible Automation", "Automate server configuration", personal_cat, medium_pri),
            ("Study Network Security", "Learn firewall and VPN configuration", school_cat, high_pri),
            ("Backup Strategy Implementation", "Set up automated database backups", work_cat, critical_pri),
            ("Learn Terraform Infrastructure as Code", "Manage cloud resources with code", personal_cat, medium_pri),
            ("Prepare Tech Interview", "Practice coding problems and system design", personal_cat, high_pri),
            ("Update LinkedIn Profile", "Add recent projects and skills", personal_cat, medium_pri),
            ("Write Technical Blog Post", "Share knowledge on programming topic", personal_cat, low_pri),
            ("Attend Tech Meetup", "Network with other developers", personal_cat, optional_pri),
            ("Learn Public Speaking", "Practice technical presentations", personal_cat, medium_pri),
            ("Contribute to Open Source", "Make PR to GitHub project", personal_cat, medium_pri),
            ("Study Software Engineering Ethics", "Learn professional responsibility", school_cat, low_pri),
        ]

        created_count = 0
        for title, description, category, priority in cs_tasks[:count]:
            deadline = timezone.now() + timedelta(days=random.randint(1, 30))
            
            task = Task.objects.create(
                title=title,
                description=description,
                status=random.choice(statuses),
                category=category,
                priority=priority,
                deadline=deadline
            )
            created_count += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully created {created_count} computer science tasks!"))

        tasks = Task.objects.all()
        for task in random.sample(list(tasks), min(20, tasks.count())):
            if random.random() > 0.5:
                SubTask.objects.create(
                    parent_task=task,
                    title=f"Research {task.title.split()[0]} concepts",
                    status=random.choice(statuses)
                )
            
            if random.random() > 0.6:
                Note.objects.create(
                    task=task,
                    content=f"Important: Remember to document progress on {task.title}"
                )

        self.stdout.write(self.style.SUCCESS("Added subtasks and notes to random tasks!"))
