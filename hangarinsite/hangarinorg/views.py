from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from hangarinorg.models import Priority, Category, Task, Note, SubTask
from hangarinorg.forms import PriorityForm, CategoryForm, TaskForm, NoteForm, SubTaskForm
from django.urls import reverse_lazy
from django.db.models import Q
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin

class HomePageView(LoginRequiredMixin, ListView):
    model = Priority
    context_object_name = 'home'
    template_name = "home.html"

    login_url = 'account_login'
    redirect_field_name = 'next'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["total_tasks"] = Task.objects.count()
        context["total_notes"] = Note.objects.count()
    
        context["pending_tasks"] = Task.objects.filter(task_status="Pending").count()
        context["completed_tasks"] = Task.objects.filter(task_status="Completed").count()
        context["in_progress_tasks"] = Task.objects.filter(task_status="In Progress").count()

        context["recent_tasks"] = Task.objects.order_by('-created_at')[:5]

        today = timezone.now().date()

        return context


# Category
class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'category'
    template_name = 'category_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(category_name__icontains=query)
        return qs

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category_form.html'
    success_url = reverse_lazy('category-list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'category_del.html'
    success_url = reverse_lazy('category-list')

# Note
class NoteList(LoginRequiredMixin, ListView):
    model = Note
    context_object_name = 'note'
    template_name = 'note_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(note_content__icontains=query)
        return qs
    
    def get_ordering(self):
        allowed = ["note_content", "created_at"]
        sort_by = self.request.GET.get("sort_by")

        if sort_by in allowed:
            return sort_by
        return "-created_at"

class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')

class NoteUpdateView(LoginRequiredMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'note_form.html'
    success_url = reverse_lazy('note-list')

class NoteDeleteView(LoginRequiredMixin, DeleteView):
    model = Note
    template_name = 'note_del.html'
    success_url = reverse_lazy('note-list')    

# Priority
class PriorityList(LoginRequiredMixin, ListView):
    model = Priority
    context_object_name = 'priority'
    template_name = 'priority_list.html'
    paginate_by = 5

class PriorityCreateView(LoginRequiredMixin, CreateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')

class PriorityUpdateView(LoginRequiredMixin, UpdateView):
    model = Priority
    form_class = PriorityForm
    template_name = 'priority_form.html'
    success_url = reverse_lazy('priority-list')

class PriorityDeleteView(LoginRequiredMixin, DeleteView):
    model = Priority
    template_name = 'priority_del.html'
    success_url = reverse_lazy('priority-list')

# Subtask
class SubTaskList(LoginRequiredMixin, ListView):
    model = SubTask
    context_object_name = 'subtask'
    template_name = 'subtask_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(sub_title__icontains=query)
        return qs
    
    def get_ordering(self):
        allowed = ["sub_title", "sub_status",]
        sort_by = self.request.GET.get("sort_by")

        if sort_by in allowed:
            return sort_by
        return "sub_title"    

class SubTaskCreateView(LoginRequiredMixin, CreateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')

class SubTaskUpdateView(LoginRequiredMixin, UpdateView):
    model = SubTask
    form_class = SubTaskForm
    template_name = 'subtask_form.html'
    success_url = reverse_lazy('subtask-list')

class SubTaskDeleteView(LoginRequiredMixin, DeleteView):
    model = SubTask
    template_name = 'subtask_del.html'
    success_url = reverse_lazy('subtask-list')

# Task
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'task'
    template_name = 'task_list.html'
    paginate_by = 5

    def get_queryset(self):
        qs = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            qs = qs.filter(task_title__icontains=query)
        return qs
    
    def get_ordering(self):
        allowed = ["task_title", "task_deadline", "task_status"]
        sort_by = self.request.GET.get("sort_by")

        if sort_by in allowed:
            return sort_by
        return "task_title"

class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['priorities'] = Priority.objects.all()
        return context
    
    def form_valid(self, form):
        print("Form is valid, saving...")
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print("Form is invalid!")
        print("Form errors:", form.errors)
        return super().form_invalid(form)

class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'task_form.html'
    success_url = reverse_lazy('task-list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['priorities'] = Priority.objects.all()
        return context

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'task_del.html'
    success_url = reverse_lazy('task-list')
    