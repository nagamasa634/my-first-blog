from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import Postform
from django.utils import timezone

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')
    return render(request, 'myblog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk = pk)
    return render(request, 'myblog/post_detail.html', {'post':post})

def post_new(request):
    if request.method == "POST":
        form = Postform(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = Postform()
    return render(request, 'myblog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk = pk)
    if request.method == "POST":
        form = Postform(request.POST, instance = post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = Postform(instance=post)
    return render(request, 'myblog/post_edit.html', {'form':form})

def post_remove(request, pk):
    post = get_object_or_404(Post, pk = pk)
    if request.method == "POST":
        post.delete()
    return redirect('post_list')