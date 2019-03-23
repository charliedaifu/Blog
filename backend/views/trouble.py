from django.shortcuts import render,redirect,HttpResponse
from django.db.models import Q
from django.db import connection
from django.urls import reverse
from utils.pager import Pagination
from repository.models import *
from backend.forms import *
import datetime
import json


def trouble_list(request,**kwargs):
    '''显示报障单'''
    # 分页
    current_user = request.session.get('username')
    base_url = reverse('trouble', kwargs=kwargs)
    data_count = Trouble.objects.filter(user__username=current_user).count()
    trouble_list = Trouble.objects.filter(user__username=current_user).order_by('status').only('id','title','status','ctime','processer')
    page_obj = Pagination(data_count, request.GET.get('p'))
    data = trouble_list[page_obj.start():page_obj.end()]
    page_str = page_obj.page_str(base_url)
    return render(
        request,
        'backend_trouble_list.html',
        {
            'title': '后台管理',
            'data': data,
            'page_str':page_str,
        }
    )

def trouble_create(request):
    '''创建报障单'''
    current_user = request.session.get('username')
    user_obj = UserInfo.objects.filter(username=current_user).first()
    if request.method == 'GET':
        form = TroubleMaker()
    else:
        form = TroubleMaker(request.POST)
        if form.is_valid():
            dic = {}
            dic['user_id'] = user_obj.id
            dic['ctime'] = datetime.datetime.now()
            dic['status'] = 1
            dic.update(form.cleaned_data)
            Trouble.objects.create(**dic)
            return redirect('/backend/trouble-list.html')
    return render(request, 'backend_trouble_create.html', {'form': form})

def trouble_edit(request,nid):
    '''编辑报障单'''
    if request.method == 'GET':
        obj = Trouble.objects.filter(id=nid, status=1).only('id', 'title', 'detail').first()
        if not obj:
            return HttpResponse('已处理中的报障单无法修改...')
        #initial不会触发错误验证，data才会验证
        form = TroubleMaker(initial={'title':obj.title,'detail':obj.detail})
        return render(request, 'backend_trouble_edit.html', {'form': form,'nid':nid})
    else:
        form = TroubleMaker(request.POST)
        if form.is_valid():
            #更新数据库的返回值是受影响的行数
            v = Trouble.objects.filter(id=nid, status=1).update(**form.cleaned_data)
            if not v:
                return HttpResponse('已经被处理...')
            else:
                return redirect('/backend/trouble-list.html')
        return render(request, 'backend_trouble_edit.html', {'form': form, 'nid': nid})

def trouble_kill_list(request):
    '''显示处理报障单'''
    current_user = request.session.get('username')
    user_obj = UserInfo.objects.filter(username=current_user).first()
    current_user_id = user_obj.id
    result = Trouble.objects.filter(Q(processer_id=current_user_id)|Q(status=1)).order_by('status')
    return render(request,'backend_trouble_kill_list.html',{'result':result})

def trouble_kill(request,nid):
    '''处理报障单'''
    current_user = request.session.get('username')
    user_obj = UserInfo.objects.filter(username=current_user).first()
    current_user_id = user_obj.id
    if request.method == 'GET':
        # 如果ret为真，说明当前订单已经是自己的了
        ret = Trouble.objects.filter(id=nid,processer=current_user_id).count()
        print(ret)
        if not ret:   #如果订单还不是自己的,就把订单处理者改成自己
            v = Trouble.objects.filter(id=nid,status=1).update(processer=current_user_id,status=2)
            print(v)
            if not v:  # 如果更新失败，说明订单已经被别人抢走了
                return HttpResponse('手速太慢了...')
        print('抢到订单')
        # 如果订单处理者已经是自己了，就执行以下代码
        obj = Trouble.objects.filter(id=nid).first()
        form = TroubleKill(initial={'title':obj.title,'solution':obj.solution})
        trouble_templates = TroubleTemplates.objects.all()
        return render(
            request,
            'backend_trouble_kill.html',
            {
                'form': form,
                'nid':nid,
                'trouble_templates':trouble_templates,
            }
        )
    else:
        ret = Trouble.objects.filter(id=nid, processer=current_user_id,status=2).count()
        if not ret:
            return HttpResponse('不是你的订单，不要乱来...')
        form = TroubleKill(request.POST)
        if form.is_valid():
            dic = {}
            dic['ptime'] = datetime.datetime.now()
            dic['status'] = 3
            dic['solution'] = form.cleaned_data['solution']
            Trouble.objects.filter(id=nid, processer=current_user_id,status=2).update(**dic)
            return redirect('/backend/trouble-kill-list.html')
        return render(request, 'backend_trouble_kill.html', {'form': form, 'nid': nid})


def trouble_report(request,**kwargs):
    '''故障处理报告:超级管理员才能看到'''
    # 分页
    base_url = reverse('report', kwargs=kwargs)
    data_count = Trouble.objects.all().count()
    trouble_list = Trouble.objects.filter().order_by('status').only('id', 'title', 'status', 'ctime', 'processer')
    page_obj = Pagination(data_count, request.GET.get('p'))
    data = trouble_list[page_obj.start():page_obj.end()]
    page_str = page_obj.page_str(base_url)
    return render(
        request,
        'backend_trouble_report.html',
        {
            'data': data,
            'page_str': page_str,
        }
    )

def trouble_json_report(request):
    '''数据库中获取数据'''
    user_list = UserInfo.objects.filter()
    response = []
    for user in user_list:
        cursor = connection.cursor()
        #需要将格式化后的年月格式化成时间戳格式
        cursor.execute(
            """SELECT strftime('%%s',strftime("%%Y-%%m-01",ptime))*1000,count(id) from repository_trouble where processer_id = %s group by strftime("%%Y-%%m",ptime)""",
            [user.id,]
        )
        result = cursor.fetchall()
        temp = {
            'name':user.username,
            'data':result,
        }
        response.append(temp)
    print(response)
    return HttpResponse(json.dumps(response))
