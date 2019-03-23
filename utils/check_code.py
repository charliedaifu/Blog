from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageFilter
import random
import math
import string
import os

BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class CreateCheckCode:
    #生成几位数的验证码
    number = 4
    #生成验证码图片的高度和宽度
    size = (100,30)
    #背景颜色，默认为白色
    bg_color = (255,255,255)
    #字体颜色，默认为蓝色
    font_color = (0,0,255)
    #干扰线颜色。默认为红色
    line_color = (255,0,0)
    #是否要加入干扰线
    draw_line = True
    #加入干扰线条数的上下限
    line_number = (1,5)
    #字体路径和保存路径
    font_path = os.path.join(BASE_PATH, 'static/font/Monaco.ttf')
    save_path = os.path.join(BASE_PATH, 'static/img/check_code')

    def create_str(self):
        '''生成字符串:字母+数字'''
        source = list(string.ascii_letters)
        for index in range(0, 10):
            source.append(str(index))
        return ''.join(random.sample(source, self.number))

    def create_lines(self,draw,width,height):
        '''绘制干扰线'''
        begin = (random.randint(0, width), random.randint(0, height))
        end = (random.randint(0, width), random.randint(0, height))
        draw.line([begin, end], fill=self.line_color)

    def check_code(self, filename):
        width, height = self.size
        image = Image.new('RGBA', self.size, self.bg_color)  # 创建空白图片
        font = ImageFont.truetype(self.font_path, 25)  # 验证码的字体和字体大小
        draw = ImageDraw.Draw(image)  # 创建画笔
        text = self.create_str()  # 生成字符串
        # print('字符串：',text)
        font_width, font_height = font.getsize(text)
        # 填充字符串
        draw.text(((width - font_width)/self.number,(height-font_height)/self.number),text,font=font,fill=self.font_color)
        if self.draw_line:
            self.create_lines(draw, width, height)
            self.create_lines(draw, width, height)
            self.create_lines(draw, width, height)
        # 创建扭曲
        image = image.transform((width + 20, height + 10), Image.AFFINE, (1, -0.3, 0, -0.1, 1, 0), Image.BILINEAR)
        # 滤镜，边界加强
        image = image.filter(ImageFilter.EDGE_ENHANCE_MORE)
        # 保存验证码图片.png
        image.save('%s/%s.png' % (self.save_path, filename))
        # print("图片保存路径:", self.save_path)
        return text

#字体文件路径
# obj = CreateCheckCode()
# obj.check_code('01')



