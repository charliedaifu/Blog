from django.db import models

class UserInfo(models.Model):
    '''用户信息'''
    username = models.CharField(max_length=32,verbose_name='用户名')
    pwd = models.CharField(max_length=32,verbose_name='密码')
    email = models.EmailField(max_length=32)
    # img报错：NOT NULL constraint failed
    # img = models.ImageField(upload_to='static/img/head_portrait',verbose_name='头像路径',null=True,blank=True,default='/')
    fans = models.ManyToManyField('UserInfo',related_name='star', verbose_name='粉丝')
    class Meta:
        verbose_name_plural = '用户信息'
    def __str__(self):
        return self.username


class Blog(models.Model):
    '''个人博客信息'''
    title = models.CharField(max_length=100, verbose_name='标题')
    summary = models.CharField(max_length=256, verbose_name='简介')
    suffix = models.CharField(max_length=32, verbose_name='个人博客后缀',unique=True)
    theme_choice = [
        (1,'warm'),
        (2,'cold'),
    ]
    theme = models.IntegerField(max_length=32, verbose_name='博客主题',choices=theme_choice,default=1)
    user = models.OneToOneField('UserInfo',on_delete=models.CASCADE,verbose_name='用户')
    class Meta:
        verbose_name_plural = '个人博客信息'
    def __str__(self):
        return self.suffix

class Article(models.Model):
    '''文章信息'''
    title = models.CharField(max_length=100,verbose_name='标题')
    summary = models.CharField(max_length=256,verbose_name='简介')
    pub_date = models.DateTimeField(auto_now_add=True,verbose_name='发布时间')
    img = models.ImageField(upload_to='static/img/news', verbose_name='图片路径')
    # up_count = models.IntegerField(default=0,verbose_name='赞个数')
    # down_count = models.IntegerField(default=0,verbose_name='踩个数')
    classification = models.ForeignKey('Classification', verbose_name='文章分类', on_delete=models.CASCADE, null=True, blank=True)
    author = models.ForeignKey('UserInfo', on_delete=models.CASCADE, verbose_name='文章作者')
    class Meta:
        verbose_name_plural = '文章'
    def __str__(self):
        return self.title

class ArticleMoreInfo(models.Model):
    '''文章更多信息'''
    content = models.TextField(verbose_name='文章内容')
    article = models.OneToOneField('Article',on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = '文章内容'
    def __str__(self):
        return self.article.title


class Classification(models.Model):
    '''文章分类'''
    name = models.CharField(max_length=32, verbose_name='名称')
    blog = models.ForeignKey('Blog',verbose_name='所属博客',on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = '文章分类'
    def __str__(self):
        return self.name


class Comment(models.Model):
    '''文章评论表'''
    content = models.CharField(max_length=128,verbose_name='评论内容')
    article = models.ForeignKey('Article',on_delete=models.CASCADE,verbose_name='文章')
    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE,verbose_name='评论者')
    parent_comment = models.ManyToManyField('Comment',related_name='last',verbose_name='上一级评论')
    class Meta:
        verbose_name_plural = '文章评论表'
    def __str__(self):
        return self.user.username

# class PraiseTread(models.Model):
#     '''赞踩表'''
#     article = models.ManyToManyField('Article',verbose_name='文章')
#     user = models.ManyToManyField('UserInfo',verbose_name='用户')
#     praise_or_tread = models.BooleanField(verbose_name='赞或踩')
#     class Meta:
#         verbose_name_plural = '赞踩表'
#         # 一个用户对同一篇文章进行只能赞或踩其中一个
#         unique_together = (("article", "user"),)
#     def __str__(self):
#         return self.praise_or_tread


class Trouble(models.Model):
    '''报障单'''
    title = models.CharField(max_length=32)
    detail = models.TextField()
    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE,related_name='u')
    # ctime = models.CharField(max_length=32)  #时间戳
    ctime = models.DateTimeField()
    status_choices = (
        (1,'未处理'),
        (2,'处理中'),
        (3,'已处理'),
    )
    status = models.IntegerField(choices=status_choices,default=1)
    processer = models.ForeignKey('UserInfo',on_delete=models.CASCADE,related_name='p',null=True,blank=True)
    solution = models.TextField(null=True)
    ptime = models.DateTimeField(null=True)
    evaluate_choices = (
        (1, '不满意'),
        (2, '一般'),
        (3, '满意'),
    )
    evaluate = models.IntegerField(choices=evaluate_choices, default=2,null=True)
    class Meta:
        verbose_name_plural = '报障单'
    def __str__(self):
        return self.title

class TroubleTemplates(models.Model):
    '''解决方案模板'''
    title = models.CharField(max_length=32)
    content = models.TextField()
    class Meta:
        verbose_name_plural = '解决方案模板'
    def __str__(self):
        return self.title

