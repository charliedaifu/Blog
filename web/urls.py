from django.conf.urls import url
from web.views import home
from web.views import account

urlpatterns = [
    # 博客主页
    url(r'^$', home.index),

    # 测试kindeditor
    url(r'^upload_img.html$', home.upload_img),
    url(r'^upload.html$', home.upload),

    # 博客主页导航栏分类显示
    url(r'^all/(?P<classification_id>\d+).html', home.index,name='index'),
    # 登陆页面
    url(r'^login.html$', account.login),
    # 注册页面
    url(r'^register.html$', account.register),
    # 注销页面
    url(r'^logout.html$', account.logout),
    # 点击生成验证码
    url(r'^check_code.html$', account.check_code),
    # 个人博客主页
    url(r'^(?P<suffix>\w+).html$', home.personal_homepage,name='user_home'),
    # 个人文章最终页
    url(r'^(?P<suffix>\w+)/(?P<id>\d+).html$', home.article),
    # 个人文章按分类、日期显示
    url(r'^(?P<suffix>\w+)/(?P<condition>((category)|(date)))/(?P<val>\w+-*\w*).html$', home.filter,name='filter'),
]