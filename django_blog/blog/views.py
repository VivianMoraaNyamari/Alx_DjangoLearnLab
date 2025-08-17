from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from .forms import CustomUserCreationForm, ProfileEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm, CommentForm
from django.urls import reverse, reverse_lazy
from django.db.models import Q

def home_view(request):
    return render(request, 'blog/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('blog:home')
        
    else:
        form = CustomUserCreationForm()

    return render(request, 'blog/register.html', {'form': form})
    
@login_required
def profile(request):
    return render(request, 'blog/profile.html')

def profile_edit(request):
    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile')

    else:
        form = ProfileEditForm(instance=request.user)

    return render(request, 'blog/profile_edit.html', {'form': form})

def login_user(request):
    return LoginView.as_view(template_name='blog/login.html')(request)

def logout_user(request):
    logout(request)
    return redirect('blog:home')

class PostListView(ListView):
    """
    Displays a list of all blog posts.
    """
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

class PostDetailView(DetailView):
    """
    Views details of a specific blog post.
    """
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(post=self.object).order_by('-created_at')
        context['form'] = CommentForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Allows users to create new blog posts.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def form_valid(self, form): # Overrides the form_valid method to automatically set the auther's name
        # Tells the form not to commit to the database
        form.instance.author = self.request.user
        # Saves the form before proceeding with the rest of the logic
        return super().form_valid(form)
    
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """"
    Allows user to update their blog posts.
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def test_func(self):
        # The functions return True if the user is the post's author
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """"
    Allows only users to delete their own blog posts
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/' # Returns back to the post_list url

    def test_func(self):
        # Ensures only the post's author can delete the blog post
        post = self.get_object()
        return self.request.user == post.author
    
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        # We get the post object using the 'post_id' from the URL.
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))

        # We manually set the post and author fields on the comment instance.
        form.instance.post = post
        form.instance.author = self.request.user

        # The parent method saves the form and handles the redirect.
        return super().form_valid(form)
    
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def get_success_url(self):
        # Redirect to the post detail page after updating the comment
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        # Ensure only the comment's author can update the comment
        comment = self.get_object()
        return self.request.user == comment.author
    
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def get_success_url(self):
        # Redirect to the post detail page after deleting the comment
        return reverse('blog:post_detail', kwargs={'pk': self.object.post.pk})

    def test_func(self):
        # Ensure only the comment's author can delete the comment
        comment = self.get_object()
        return self.request.user == comment.author
    
# Tag-filtered view: Displays posts with a specific tag
class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        # We get the tag_slug from the URL.
        tag_slug = self.kwargs['tag_slug']
        # We filter the queryset to only include posts that have this tag.
        return Post.objects.filter(tags__slug__in=[tag_slug])

# Search view: A function-based view for handling search queries
def search_posts(request):
    query = request.GET.get('q', '')  # Get the search query from the URL parameter 'q'
    results = Post.objects.all()

    if query:
        # Use Q objects for OR queries on multiple fields.
        # __icontains is a case-insensitive lookup.
        results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()
    
    context = {
        'query': query,
        'posts': results,
    }
    return render(request, 'blog/search_results.html', context)
