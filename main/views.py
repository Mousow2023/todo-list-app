# from django.forms import BaseModelForm
# from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, DeleteView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task

# Create your views here.
class CustomLoginView(LoginView):
    template_name = "main/login.html"
    fields = "__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("index")

class RegisterView(FormView):
    form_class  = UserCreationForm
    template_name = "main/register.html"
    redirect_authenticated_user = True
    success_url = reverse_lazy("index")

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("index")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user) #Log the user in
        return super().form_valid(form)



class TaksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = "main/tasks_list.html"
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(is_completed=False).count()

        search_input = self.request.GET.get("search-input") or ""
        if search_input:
            context["tasks"] = context["tasks"].filter(title__startswith=search_input)
        context["searched"] = search_input
        
        return context


class TaksDetailView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "main/single_task.html"
    context_object_name = "task"


class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = "main/create_task.html"
    fields = ["title", "description", "is_completed"]
    success_url = reverse_lazy("index")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class UpdateTaskView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = "main/create_task.html"
    fields = ["title", "description", "is_completed"]
    success_url = reverse_lazy("index")


class DeleteTaskView(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = "main/delete_task.html"
    context_object_name = "task"
    success_url = reverse_lazy("index")