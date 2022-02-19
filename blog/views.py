from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import Article, Comment
from django.contrib.auth.decorators import login_required
# Create your views here.


def index(request):
    articles = Article.objects.all()
    return render(request, 'blog/index.html', {'articles': articles})


@login_required(login_url='signin')
def new(request):
    if request.method == 'POST':
        article = Article.objects.create(
            author=request.user,
            title=request.POST['title'],
            content=request.POST['content']
        )
        return redirect('detail', article.pk)
    else:
        return render(request, 'blog/new.html')


@login_required(login_url='signin')
def detail(request, pk): # 사용자가 어떤 글을 보고자 했는지를 받아줘야하기 때문
    article = Article.objects.get(pk=pk) # 왼쪽 pk 필드명 , 오른쪽 pk 변수명
    if request.method == 'POST':
        comment = Comment.objects.create(
            author=request.user,
            article=article,
            comment=request.POST['comment']
        )
        return redirect('detail', article.pk)
    else:
        comments = Comment.objects.filter(article=article)
        return render(request, 'blog/detail.html', {'article':article, 'comments':comments})


@login_required(login_url='signin')
def edit(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.author:
        if request.method == 'POST':
            article.title = request.POST['title']
            article.content = request.POST['content']
            article.save()
            return redirect('detail', article.pk)
        else:
            return render(request, 'blog/edit.html', {'article':article})
    else:
        return render(request, 'blog/edit.html', {'error':'잘못된 접근입니다.'})


@login_required(login_url='signin')
def delete(request, pk):
    article = Article.objects.get(pk=pk)
    if request.user == article.author:
        article.delete()
        return redirect('index')
    else:
        return redirect('detail', article.pk)


@login_required(login_url='signin')
def delete_comment(request, article_pk, comment_pk):
    comment = Comment.objects.get(pk=comment_pk)
    if request.user == comment.author:
        comment.delete()
        return redirect('detail', article_pk)
    else:
        return redirect('detail', article_pk)