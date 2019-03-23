from django.conf.urls import url
from backend.views import user
from backend.views import trouble

urlpatterns = [
    url(r'^$', user.backend),
    url(r'^article_management.html$', user.article),
    url(r'^category_management.html$', user.category),

    #一般用户:提交报障单，查看，修改（未处理时），评价（处理完成，未评分）
    url(r'^trouble-list.html$', trouble.trouble_list,name='trouble'),
    url(r'^trouble-create.html$', trouble.trouble_create),
    url(r'^trouble-edit-(\d+).html$', trouble.trouble_edit),
    #处理者
    url(r'^trouble-kill-list.html$', trouble.trouble_kill_list),
    url(r'^trouble-kill-(\d+).html$', trouble.trouble_kill),
    url(r'^trouble-report.html$', trouble.trouble_report,name='report'),
    url(r'^trouble-json-report.html$', trouble.trouble_json_report),
]
