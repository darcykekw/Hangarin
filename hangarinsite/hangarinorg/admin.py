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
    
    date_hierarchy = "deadline"


@admin.register(SubTask)
class SubTaskAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "parent_task_name")
    search_fields = ("title",)
    list_filter = ("status",)
    
    def parent_task_name(self, obj):
        return obj.parent_task.title
    parent_task_name.short_description = "Parent Task"
    
    def parent_task_name(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        url = reverse('admin:hangarinorg_task_change', args=[obj.parent_task.id])
        return format_html('<a href="{}">{}</a>', url, obj.parent_task.title)
    parent_task_name.short_description = "Parent Task"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    list_display_links = ("name",)
    
    list_filter = ("created_at", "updated_at")


@admin.register(Priority)
class PriorityAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
    search_fields = ("name",)
    list_display_links = ("name",)
    
    list_filter = ("created_at", "updated_at")


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("task", "truncated_content", "created_at")
    search_fields = ("content", "task__title")
    list_filter = ("created_at", "task")
    
    date_hierarchy = "created_at"
    
    def truncated_content(self, obj):
        if len(obj.content) > 50:
            return f"{obj.content[:50]}..."
        return obj.content
    truncated_content.short_description = "Content"
    
    def task_link(self, obj):
        from django.utils.html import format_html
        from django.urls import reverse
        url = reverse('admin:hangarinorg_task_change', args=[obj.task.id])
        return format_html('<a href="{}">{}</a>', url, obj.task.title)
    task_link.short_description = "Task"
