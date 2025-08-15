from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from .models import TaskType, Position, Worker, Task, Tag
from django.db.models import QuerySet
from django.shortcuts import get_object_or_404
from .forms import TaskForm


@login_required
def index(request) -> HttpResponseRedirect:
    """View function for the home page of the site."""

    num_worker = Worker.objects.count()
    num_task = Task.objects.count()
    num_tasktype = TaskType.objects.count()
    num_position = Position.objects.count()

    num_visits = request.session.get("num_visits", 0)
    request.session["num_visits"] = num_visits + 1

    context = {
        "num_worker": num_worker,
        "num_task": num_task,
        "num_tasktype": num_tasktype,
        "num_position": num_position + 1,
    }

    return render(request, "company/index.html", context=context)


class TaskTypeListView(LoginRequiredMixin, generic.ListView):
    model = TaskType
    context_object_name = "task-type_list"
    template_name = "company/task-type_list.html"
    paginate_by = 5


class TaskTypeCreateView(LoginRequiredMixin, generic.CreateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("company:task-type-list")


class TaskTypeUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = TaskType
    fields = "__all__"
    success_url = reverse_lazy("company:task-type-list")


class TaskTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = TaskType
    success_url = reverse_lazy("company:task-type-list")


class TaskSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="Search by name",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search by name"})
    )
    tag = forms.CharField(
        max_length=100,
        required=False,
        label="Search by tags",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Search by tags"})
    )


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    context_object_name = "position_list"
    template_name = "company/position-list.html"
    paginate_by = 5


class PositionCreateView(LoginRequiredMixin, generic.CreateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("company:position-list")


class PositionUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Position
    fields = "__all__"
    success_url = reverse_lazy("company:position-list")


class PositionDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("company:position-list")


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=False,
        label="Search by name"
    )


class TaskListView(LoginRequiredMixin, generic.ListView):
    model = Task
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs) -> dict:
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        tag = self.request.GET.get("tag", "")
        context["search_form"] = TaskSearchForm(initial={"name": name, "tag": tag})
        return context

    def get_queryset(self) -> QuerySet:
        queryset = Task.objects.select_related("task_type").prefetch_related("tags")
        form = TaskSearchForm(self.request.GET)
        if form.is_valid():
            name = form.cleaned_data.get("name")
            tag = form.cleaned_data.get("tag")
            if name:
                queryset = queryset.filter(name__icontains=name)
            if tag:
                queryset = queryset.filter(tags__name__icontains=tag)
        return queryset


class TaskDetailView(LoginRequiredMixin, generic.DetailView):
    model = Task


class TaskCreateView(LoginRequiredMixin, generic.CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("company:task-list")


class TaskUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("company:task-list")


class TaskDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Task
    success_url = reverse_lazy("company:task-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    paginate_by = 5


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("tasks__task_type", "tasks__tags")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        worker = self.get_object()
        completed_tasks = worker.tasks.filter(is_completed=True).order_by("-deadline")
        incomplete_tasks = worker.tasks.filter(is_completed=False).order_by("deadline")  # <-- Виправлено
        context["completed_tasks"] = completed_tasks
        context["incomplete_tasks"] = incomplete_tasks
        return context


class WorkerCreationForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = "__all__"


class WorkerCreateView(LoginRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("company:worker-list")


class WorkerLicenseUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = "__all__"


class WorkerLicenseUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerLicenseUpdateForm
    success_url = reverse_lazy("company:worker-list")


class WorkerDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("company:worker-list")


@login_required
def toggle_assign_to_worker(request, pk) -> HttpResponseRedirect:
    worker = request.user
    task = get_object_or_404(Task, pk=pk)

    if worker in task.assignees.all():
        task.assignees.remove(worker)
    else:
        task.assignees.add(worker)

    return HttpResponseRedirect(reverse_lazy("company:task-detail", args=[pk]))


def task_list_view(request):
    filtered_tasks = Task.objects.filter(is_completed=False).order_by("priority", "deadline")

    context = {
        "tasks": filtered_tasks
    }
    return render(request, "templates/task_list.html", context)


class TagListView(LoginRequiredMixin, generic.ListView):
    model = Tag
    context_object_name = "tag_list"
    template_name = "company/tag_list.html"
    paginate_by = 5


class TagCreateView(LoginRequiredMixin, generic.CreateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("company:tag-list")


class TagUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Tag
    fields = "__all__"
    success_url = reverse_lazy("company:tag-list")


class TagDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Tag
    success_url = reverse_lazy("company:tag-list")
