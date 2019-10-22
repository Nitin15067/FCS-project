from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView
from .models import feed
from django.urls import reverse_lazy
from account.models import Account


def home_view(request):
	# random_text = "This is home view"
    context = {
        'posts': feed.objects.all()
    }
    if request.user.is_authenticated:
        return render(request, 'home.html', context)
    else:
        return redirect('login')

class PostListView(LoginRequiredMixin, ListView):
    model = feed
    template_name = 'home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    login_url = "login"
    def get_queryset(self, *args, **kwargs):
     return feed.objects.all().filter(post_to=self.request.user).order_by('-date_posted')

class PostCreateView(LoginRequiredMixin, CreateView):
    model = feed
    template_name = 'feed_form.html'
    fields = ['content','post_to']
    success_url = reverse_lazy('home')
    login_url = "login"

    def get_form(self):
        form = super(PostCreateView, self).get_form()
        initial_base = self.get_initial() 
        # initial_base['menu'] = Menu.objects.get(id=1)
        form.initial = initial_base
        form.fields['post_to'].queryset = Account.objects.all()
        return form

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form) 

