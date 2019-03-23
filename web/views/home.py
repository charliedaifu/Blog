from django.shortcuts import render,redirect
from repository.models import *
from utils.pager import Pagination
from django.urls import reverse
from web.forms import *
from django.db.models import Count
from django.db import connection
from django.http import JsonResponse
import os


def index(request,*args,**kwargs):
    '''
    博客网站主页
    :param kwargs: ｛article_type_id:1｝
    :return: index.html
    '''
    article_type_list = Classification.objects.values('id','name')
    # print(kwargs)
    # print(type(article_type_list[0]['id']))
    if kwargs:
        classification_id = int(kwargs['classification_id'])
        #reverse通过别名反向生成URL
        base_url = reverse('index',kwargs=kwargs)#all/1.html
    else:
        classification_id = None
        base_url = '/'  #/
    data_count = Article.objects.filter(**kwargs).count()
    article_list = Article.objects.filter(**kwargs).order_by('-id')#文章对象列表倒序排列，最新的在最前面
    page_obj = Pagination(data_count,request.GET.get('p'))
    data = article_list[page_obj.start():page_obj.end()]
    page_str = page_obj.page_str(base_url)

    return render(
        request,
        'index.html',
        {
            'article_type_list':article_type_list,
            'classification_id':classification_id,
            'data':data,
            'page_str':page_str,
        }
    )

def personal_homepage(request,*args,**kwargs):
    '''个人博客主页'''
    if kwargs['suffix']:
        current_user = request.session.get('username')
        user_id = request.session.get('user_id')
        base_url = reverse('user_home', kwargs=kwargs)  # /charlie2.html
        #分页
        data_count = Article.objects.filter(author__username=current_user).count()
        article_list = Article.objects.filter(author__username=current_user).order_by('-id')  # 文章对象列表倒序排列，最新的在最前面
        page_obj = Pagination(data_count, request.GET.get('p'))
        data = article_list[page_obj.start():page_obj.end()]
        page_str = page_obj.page_str(base_url)

        #分组查询,时间按年月查询，需要截取，复杂的SQL语句Django无法实现，需要原生SQL
        #mysql把strftime更换为date_format即可
        cursor = connection.cursor()
        cursor.execute(
            """select id ,count(id) as num,strftime("%Y-%m",pub_date) as ctime from repository_article group by strftime("%Y-%m",pub_date)""",
        )
        pub_date_list = cursor.fetchall()
        # print(pub_date_list) # [(8, 5, '2019-01')]

        # 统计出每个分类的ID、name、个数
        article_category_list = Article.objects.filter(author__username=current_user).\
            values('classification_id','classification__name').annotate(number=Count('title'))
        # print(article_category_list)

        # 粉丝个数
        fans_num = UserInfo.objects.filter(username=current_user).values('username','fans__username').count()
        # 关注个数
        user_obj = UserInfo.objects.filter(username=current_user).first()
        attention_num = UserInfo.objects.filter(fans__id=user_obj.id).count()

        return render(
            request,
            'personal_homepage.html',
            {
                'username':current_user,
                'data': data,
                'page_str': page_str,
                'pub_date_list': pub_date_list,
                'article_category_list': article_category_list,
                'fans_num':fans_num,
                'attention_num':attention_num,
            }
        )

def filter(request,*args,**kwargs):
    '''个人博客主页分类显示'''
    if kwargs['suffix']:
        current_user = request.session.get('username')
        condition = kwargs['condition']
        val = kwargs['val']
        base_url = reverse('filter', kwargs=kwargs)
        if condition == 'category':
            article_list = Article.objects.filter(author__username=current_user,classification_id=val).all()
        elif condition == 'date':
            article_list = Article.objects.filter(author__username=current_user).extra(
                where=['strftime("%%Y-%%m",pub_date)=%s'],params=[val,]).all()
        else:
            article_list = []
        # print(article_list)

        # 时间分组
        cursor = connection.cursor()
        cursor.execute(
            """select id ,count(id) as num,strftime("%Y-%m",pub_date) as ctime from repository_article group by strftime("%Y-%m",pub_date)""",
        )
        pub_date_list = cursor.fetchall()
        # 分类分组
        article_category_list = Article.objects.filter(author__username=current_user). \
            values('classification_id', 'classification__name').annotate(number=Count('title'))

        # 粉丝个数
        fans_num = UserInfo.objects.filter(username=current_user).values('username', 'fans__username').count()
        # 关注个数
        user_obj = UserInfo.objects.filter(username=current_user).first()
        attention_num = UserInfo.objects.filter(fans__id=user_obj.id).count()
        return render(
            request,
            'home_summary_list.html',
            {
                'article_list':article_list,
                'username': current_user,
                'pub_date_list': pub_date_list,
                'article_category_list': article_category_list,
                'fans_num': fans_num,
                'attention_num': attention_num,
            }
        )
    else:
        return redirect('/')

def article(request,**kwargs):
    '''个人文章最终页'''
    current_user = request.session.get('username')
    article_id = kwargs['id']
    article_obj = Article.objects.filter(id=article_id,author__username=current_user).first()
    # 按日期筛选
    cursor = connection.cursor()
    cursor.execute(
        """select id ,count(id) as num,strftime("%Y-%m",pub_date) as ctime from repository_article group by strftime("%Y-%m",pub_date)""",
    )
    pub_date_list = cursor.fetchall()
    # 按分类筛选
    article_category_list = Article.objects.filter(author__username=current_user).\
        values('classification_id','classification__name').annotate(number=Count('title'))

    article_content = ArticleMoreInfo.objects.filter(article_id=article_id).first()
    # 粉丝个数
    fans_num = UserInfo.objects.filter(username=current_user).values('username', 'fans__username').count()
    # 关注个数
    user_obj = UserInfo.objects.filter(username=current_user).first()
    attention_num = UserInfo.objects.filter(fans__id=user_obj.id).count()
    return render(
        request,
        'article.html',
        {
            'article_obj':article_obj,
            'article_content':article_content,
            'username': current_user,
            'pub_date_list': pub_date_list,
            'article_category_list': article_category_list,
            'fans_num': fans_num,
            'attention_num': attention_num,
        }
    )





def upload_img(request):
    '''测试kindeditor上传图片'''
    return render(request,'upload_img.html')

def upload(request):
    '''测试kindeditor预览图片'''
    # img = request.FILES.get('img')
    # print(img)
    # # file_path = os.path.join('static','img','head_portrait',img.imgFile)
    # f = open('static/img/1.jpg', 'wb')
    # for line in img.chunks():
    #     f.write(line)
    # f.close()
    dic = {
        'error': 0,
        'url': '/static/img/head_portrait/1.jpg',
        'message': 'success...'
    }
    return JsonResponse(dic)