from django.shortcuts import render
from repository.models import *
from django.db.models import Count

def backend(request):
    return render(
        request,
        'backend_layout.html',
        {
            'request':request,
        }
    )

def category(request):
    current_user = request.session.get('username')
    type_list = Article.objects.filter(author__username=current_user).values('classification__name').annotate(
        number=Count('title'))
    return render(
        request,
        'category_management.html',
        {
            'request': request,
            'type_list': type_list,
        }
    )

def article(request):
    current_user = request.session.get('username')
    article_list = Article.objects.filter(author__username=current_user).all().order_by('-id')
    return render(
        request,
        'article_management.html',
        {
            'request': request,
            'article_list': article_list,
        }
    )