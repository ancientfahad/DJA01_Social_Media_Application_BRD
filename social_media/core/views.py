from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.views.generic import (
    ListView, CreateView, UpdateView, DeleteView
)
from django.urls import reverse_lazy
from .models import Post
from .forms import UserRegistrationForm, PostForm

from django.db.models import Q

def register(request):
    """
    Handles user registration.
    
    - If the request method is POST, validates the form and creates a new user.
    - If the form is valid, saves the user and redirects to the login page with a success message.
    - If the request method is GET, renders the registration form.
    
    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: Rendered registration page or redirect to login page.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now login.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
class HomeView(ListView):
    """
    Displays a paginated list of all posts on the home page.
    
    Attributes:
        model (Post): The model to query for posts.
        template_name (str): The template used to render the home page.
        context_object_name (str): The name of the context variable for posts.
        paginate_by (int): Number of posts per page for pagination.
    """
    model = Post
    template_name = 'core/home.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.all()

        # Filtering by date
        date_filter = self.request.GET.get('date', 'latest')
        if date_filter == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        # Filtering by media type
        media_filter = self.request.GET.get('media', 'all')
        print(f"HomeView - Media filter: {media_filter}")
        if media_filter == 'text':
            # Check for both null and empty string
            queryset = queryset.filter(Q(image__isnull=True) | Q(image=''))
            print(f"HomeView - Text-only posts: {queryset.count()}")
        elif media_filter == 'images':
            # Exclude null and empty string
            queryset = queryset.exclude(Q(image__isnull=True) | Q(image=''))
            print(f"HomeView - Image posts: {queryset.count()}")

        # Filtering by user
        user_filter = self.request.GET.get('user', '')
        if user_filter:
            queryset = queryset.filter(user__username__iexact=user_filter)

        # Search by keyword
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(content__icontains=search_query)

        print(f"HomeView - Final queryset count: {queryset.count()}")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_filter'] = self.request.GET.get('date', 'latest')
        context['media_filter'] = self.request.GET.get('media', 'all')
        context['user_filter'] = self.request.GET.get('user', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context
class UserProfileView(LoginRequiredMixin, ListView):
    """
    Displays a paginated list of posts created by the logged-in user.
    
    - Requires the user to be logged in (LoginRequiredMixin).
    - Filters posts to only include those created by the current user.
    
    Attributes:
        model (Post): The model to query for posts.
        template_name (str): The template used to render the profile page.
        context_object_name (str): The name of the context variable for posts.
        paginate_by (int): Number of posts per page for pagination.
    """
    model = Post
    template_name = 'core/profile.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(user=self.request.user)

        # Filtering by date
        date_filter = self.request.GET.get('date', 'latest')
        if date_filter == 'oldest':
            queryset = queryset.order_by('created_at')
        else:
            queryset = queryset.order_by('-created_at')

        # Filtering by media type
        media_filter = self.request.GET.get('media', 'all')
        print(f"UserProfileView - Media filter: {media_filter}")
        if media_filter == 'text':
            # Check for both null and empty string
            queryset = queryset.filter(Q(image__isnull=True) | Q(image=''))
            print(f"UserProfileView - Text-only posts: {queryset.count()}")
        elif media_filter == 'images':
            # Exclude null and empty string
            queryset = queryset.exclude(Q(image__isnull=True) | Q(image=''))
            print(f"UserProfileView - Image posts: {queryset.count()}")

        # Search by keyword
        search_query = self.request.GET.get('q', '')
        if search_query:
            queryset = queryset.filter(content__icontains=search_query)

        print(f"UserProfileView - Final queryset count: {queryset.count()}")
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['date_filter'] = self.request.GET.get('date', 'latest')
        context['media_filter'] = self.request.GET.get('media', 'all')
        context['search_query'] = self.request.GET.get('q', '')
        return context
class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Handles the creation of a new post.
    
    - Requires the user to be logged in (LoginRequiredMixin).
    - Automatically assigns the logged-in user as the post author.
    - Displays a success message upon successful post creation.
    
    Attributes:
        model (Post): The model to create a post.
        form_class (PostForm): The form used to create a post.
        template_name (str): The template used to render the post creation form.
        success_url (str): The URL to redirect to after successful post creation.
    """
    model = Post
    form_class = PostForm
    template_name = 'core/post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Assigns the logged-in user as the post author and displays a success message.
        
        Args:
            form (PostForm): The validated form instance.
        
        Returns:
            HttpResponseRedirect: Redirects to the success URL.
        """
        form.instance.user = self.request.user
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """
    Handles the updating of an existing post.
    
    - Requires the user to be logged in (LoginRequiredMixin).
    - Ensures only the post author can update the post (UserPassesTestMixin).
    - Displays a success message upon successful post update.
    
    Attributes:
        model (Post): The model to update a post.
        form_class (PostForm): The form used to update a post.
        template_name (str): The template used to render the post update form.
        success_url (str): The URL to redirect to after successful post update.
    """
    model = Post
    form_class = PostForm
    template_name = 'core/post_form.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """
        Displays a success message upon successful post update.
        
        Args:
            form (PostForm): The validated form instance.
        
        Returns:
            HttpResponseRedirect: Redirects to the success URL.
        """
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        """
        Ensures only the post author can update the post.
        
        Returns:
            bool: True if the current user is the post author, otherwise False.
        """
        post = self.get_object()
        return self.request.user == post.user
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """
    Handles the deletion of an existing post.
    
    - Requires the user to be logged in (LoginRequiredMixin).
    - Ensures only the post author can delete the post (UserPassesTestMixin).
    - Displays a success message upon successful post deletion.
    
    Attributes:
        model (Post): The model to delete a post.
        success_url (str): The URL to redirect to after successful post deletion.
        template_name (str): The template used to render the post deletion confirmation page.
    """
    model = Post
    success_url = reverse_lazy('home')
    template_name = 'core/post_confirm_delete.html'

    def test_func(self):
        """
        Ensures only the post author can delete the post.
        
        Returns:
            bool: True if the current user is the post author, otherwise False.
        """
        post = self.get_object()
        return self.request.user == post.user

    def delete(self, request, *args, **kwargs):
        """
        Displays a success message upon successful post deletion.
        
        Args:
            request (HttpRequest): The HTTP request object.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        
        Returns:
            HttpResponseRedirect: Redirects to the success URL.
        """
        messages.success(self.request, 'Post deleted successfully!')
        return super().delete(request, *args, **kwargs)