from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Priority(BaseModel):
    priority_name = models.CharField(max_length=100, verbose_name="Name")

    class Meta:
        verbose_name = "Priority"
        verbose_name_plural = "Priorities"

    def __str__(self):
        return self.priority_name 
    
class Category(BaseModel):
    category_name = models.CharField(max_length=100, verbose_name="Name")

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_name
    
class Task(BaseModel):
    task_title = models.CharField(max_length=150, verbose_name="Title")
    task_description = models.CharField(max_length=150, verbose_name="Description")
    task_deadline = models.DateField(verbose_name="Deadline")
    task_status = models.CharField(
        max_length=50,
        choices= [
            ("Pending", "Pending"),
            ("In Progress", "In Progress"),
            ("Completed", "Completed"),
        ],
        default = "pending",
        verbose_name="Status"
    )
    task_category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Task Category")
    task_priority = models.ForeignKey(Priority, on_delete=models.CASCADE, verbose_name="Task Priority")

    def __str__(self):
        return self.task_title
    
class Note(BaseModel):
    note_content = models.CharField(max_length=150, verbose_name="Content")
    note_task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="Task")

    def __str__(self):
        return self.note_content

class SubTask(BaseModel):
    sub_title = models.CharField(max_length=150, verbose_name="Title")
    sub_status = models.CharField(
        max_length=50,
        choices= [
            ("Pending", "Pending"),
            ("In Progress", "In Progress"),
            ("Completed", "Completed"),
        ],
        default = "pending",
        verbose_name="Status"
    )
    sub_parent_task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name="Parent Task")

    def __str__(self):
        return self.sub_title
