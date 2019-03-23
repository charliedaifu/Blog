from django.shortcuts import render,redirect,HttpResponse
from utils.check_code import CreateCheckCode
from repository.models import *
from web.forms import *
import hashlib,os,uuid

# BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))



def register(request):
    '''注册'''
    if request.method == 'GET':
        #自动生成input标签
        obj = RegisterForm()
        return render(request,'register.html',{'obj': obj})
    if request.method == 'POST':
        obj = RegisterForm(request.POST)
        if obj.is_valid():
            obj.cleaned_data['pwd'] = md5(obj.cleaned_data['pwd'])
            del obj.cleaned_data['pwd_confirm']
            UserInfo.objects.create(**obj.cleaned_data)
            print("验证成功",obj.cleaned_data,type(obj.cleaned_data))
            return redirect('/login.html')
        else:
            #NON_FIELD_ERRORS='__all__'整体的错误信息放在errors的all里面
            #模板语言里不支持双下划线格式，所以用obj.non_field_errors.0
            return render(request, 'register.html', {'obj': obj})

def login(request):
    '''登陆'''
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        result = {'status':False,'msg':None}
        name = request.POST.get('username')
        pwd = request.POST.get('password')
        ck_code = request.POST.get('check_code') # 用户输入的验证码
        ss_code = request.session['check_code']  # 页面生成的验证码
        user_obj = UserInfo.objects.filter(username=name).first()
        blog_obj = Blog.objects.filter(user_id=user_obj.id).first()
        # print('****************',theme_id.theme)
        if user_obj.username == name and user_obj.pwd == md5(pwd):
            if ck_code.lower() == ss_code.lower():
                request.session['user_id'] = user_obj.id
                request.session['username'] = name
                request.session['is_login']=True
                request.session['theme_id']=blog_obj.theme
                request.session['suffix']=blog_obj.suffix
                request.session['title']=blog_obj.title
                if request.POST.get("one-month"):
                    request.session.set_expiry(60*60*24*30)
                print('登陆成功')
                return redirect('http://127.0.0.1:8000')
            else:
                result['status'] = True
                result['msg'] = '验证码错误或过期'
                return render(request, 'login.html',{'result':result})
        else:
            result['msg'] = '用户名或密码错误'
            return render(request, 'login.html', {'result':result})

def logout(request):
    '''注销'''
    request.session['username'] = ''
    return redirect('http://127.0.0.1:8000')

def check_code(request):
    '''生成验证码图片'''
    check_obj = CreateCheckCode()
    nid = str(uuid.uuid4())
    text = check_obj.check_code(nid)
    file_path = os.path.join('static/img/check_code','%s.png'%nid)
    f = open(file_path,'rb')
    data = f.read()
    f.close()
    request.session['check_code'] = text
    return HttpResponse(data)  # 返回一个验证码图片到前端显示出来

def md5(pwd):
    '''密码加密'''
    hash = hashlib.md5(bytes('uu89',encoding='utf-8'))
    hash.update(bytes(pwd,encoding='utf-8'))
    return hash.hexdigest()