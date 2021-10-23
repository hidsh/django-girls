from django.shortcuts import render
from django.utils import timezone
from .models import Post

def post_list(request):
	posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
	return render(request, 'blog/post_list.html', {'posts':posts})

def post_draft_list(request):
	posts = Post.objects.filter(published_date__isnull=True).order_by('-created_date')
	return render(request, 'blog/post_draft_list.html', {'posts':posts})

def post_detail(request, pk):
	from django.shortcuts import render, get_object_or_404
	
	post = get_object_or_404(Post, pk=pk)
	return render(request, 'blog/post_detail.html', {'post': post})

def post_edit(request, pk):
	from django.shortcuts import render, get_object_or_404
	from .forms import PostForm
	from django.shortcuts import redirect
	
	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = PostForm(request.POST, instance=post)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			# post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm(instance=post)
	return render(request, 'blog/post_edit.html', {'form': form})

def post_publish(request, pk):
	from django.shortcuts import get_object_or_404
	from django.shortcuts import redirect

	post = get_object_or_404(Post, pk=pk)
	post.publish()
	return redirect('post_detail', pk=pk)

def post_remove(request, pk):
	from django.shortcuts import get_object_or_404
	from django.shortcuts import redirect

	post = get_object_or_404(Post, pk=pk)
	post.delete()
	return redirect('post_list')

def post_new(request):
	from .forms import PostForm
	from django.shortcuts import redirect

	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.author = request.user
			post.published_date = timezone.now()
			post.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = PostForm()
	return render(request, 'blog/post_edit.html', {'form': form})

def add_comment_to_post(request, pk):
	from django.shortcuts import render, get_object_or_404
	from django.shortcuts import redirect
	from .forms import CommentForm

	post = get_object_or_404(Post, pk=pk)
	if request.method == "POST":
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.save()
			return redirect('post_detail', pk=post.pk)
	else:
		form = CommentForm()
	return render(request, 'blog/add_comment_to_post.html', {'form': form})

from django.contrib.auth.decorators import login_required
from .models import Comment

@login_required
def comment_approve(request, pk):
	from django.shortcuts import get_object_or_404
	from django.shortcuts import redirect

	comment = get_object_or_404(Comment, pk=pk)
	comment.approve()
	return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
	from django.shortcuts import get_object_or_404
	from django.shortcuts import redirect

	comment = get_object_or_404(Comment, pk=pk)
	comment.delete()
	return redirect('post_detail', pk=comment.post.pk)


