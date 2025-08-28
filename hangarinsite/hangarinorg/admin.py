from django.contrib import admin
from .models import Category, Priority, Task, SubTask, Note

class SubTaskInline(admin.TabularInline):
    model = SubTask
    extra = 1
    fields = ("title", "status")
    show_change_link = True

class NoteInline(admin.StackedInline):
    model = Note
    extra = 1
    fields = ("content", "created_at")
    readonly_fields = ("created_at",)

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "deadline", "priority", "category")
    search_fields = ("title", "description")
    list_filter = ("status", "priority", "category")
    inlines = [SubTaskInline, NoteInline]

@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "parent_task_name")
    search_fields = ("title",)
    list_filter = ("status",)
    
    def parent_task_name(self, obj):
        return obj.parent_task.title
    parent_task_name.short_description = "Parent Task"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("task", "truncated_content", "created_at")
    search_fields = ("content",)
    list_filter = ("created_at",)
    
    def truncated_content(self, obj):
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    truncated_content.short_description = "Content"