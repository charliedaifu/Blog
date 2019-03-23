from django import forms
from django.forms import fields,widgets
from repository.models import *
from django.core.exceptions import ValidationError,NON_FIELD_ERRORS
import re

class RegisterForm(forms.Form):
    '''注册验证'''
    username = fields.CharField(
        min_length=6,
        max_length=32,
        required=True,
        label='用户名',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_length':'用户名太短',
            'max_length':'用户名过长',
            'required':'用户名不能为空',
        }
    )
    pwd = fields.CharField(
        min_length=8,
        max_length=32,
        required=True,
        label='密码',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_length': '密码太短',
            'max_length': '密码过长',
            'required': '密码不能为空',
            'invalid': '密码必须包含字母、数字'
        }
    )
    pwd_confirm = fields.CharField(
        min_length=8,
        max_length=32,
        required=True,
        label='密码',
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'min_length': '密码太短',
            'max_length': '密码过长',
            'required': '密码不能为空',
            'invalid': '密码必须包含字母、数字'
        }
    )
    email = fields.EmailField(
        min_length=8,
        required=True,
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        error_messages={
            'required': '邮箱不能为空',
            'invalid': '邮箱格式错误'
        }
    )
    def clean_username(self):
        user = self.cleaned_data['username']
        if UserInfo.objects.filter(username=user).count():
            # 如果用户名已经存在
            raise ValidationError('用户名已存在')
        return user

    def clean_pwd(self):
        pwd = self.cleaned_data['pwd']
        # 字母数字下划线
        pwd_regex = r'(?!^[a-zA-Z]+$)(?!^\d+$)(?!^_+$)[0-9a-zA-Z_]{8,}'
        ret = re.compile(pwd_regex)
        if ret.match(pwd):
            return pwd
        else:
            raise ValidationError('密码必须包含至少1个字母和1个数字')

    def clean(self):
        # Django的整体错误信息放在__all__中,NON_FIELD_ERRORS='__all__'
        v1 = self.cleaned_data.get('pwd')
        v2 = self.cleaned_data.get('pwd_confirm')
        if v1 == v2:
            print('密码输入一致')
        else:
            raise ValidationError('密码前后不一致，请重新输入')

'''土鳖解决方法
    def clean(self):
        #Django的整体错误信息放在__all__中
        # value_dict = self.cleaned_data
        print(self.cleaned_data)
        v1 = self.cleaned_data.get('pwd')
        v2 = self.cleaned_data.get('pwd_confirm')
        if v1 and v1 == v2:
            # 验证完以后就删除pwd2，否则报错
            del self.cleaned_data['pwd_confirm']
            print(self.cleaned_data)
            return self.cleaned_data
        else:
            self.add_error('pwd_confirm', "密码前后不一致，请重新输入")
            raise ValidationError('密码前后不一致，请重新输入')
'''





