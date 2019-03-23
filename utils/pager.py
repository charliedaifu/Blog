class Pagination(object):
    def __init__(self,total_count,current_page,per_page_item_num=20,max_page_num=7):
        #数据总条目
        self.total_count = total_count
        #当前页
        try:
            v = int(current_page)
            if v <= 0:
                v = 1
            self.current_page = v
        except Exception as e:
            self.current_page = 1
        #每页显示条目
        self.per_page_item_num = per_page_item_num
        #每页最多显示页码
        self.max_page_num = max_page_num

    def start(self):
        return (self.current_page-1)*self.per_page_item_num

    def end(self):
        return self.current_page*self.per_page_item_num

    @property
    def num_pages(self):
        # 总页数
        a,b = divmod(self.total_count,self.per_page_item_num)
        if b == 0:
            return a
        return a+1

    def page_num_range(self):
        #如果总页数小于每页最多显示页码数量，就显示1-总页码
        if self.num_pages < self.max_page_num:
            return range(1,self.num_pages+1)
        #如果总页数有很多
        part = int(self.max_page_num/2)
        if self.current_page <= part:
            return range(1,self.max_page_num+1)
        #最后一页只显示最后10个页码即可
        if (self.current_page+part) > self.num_pages:
            return range(self.num_pages-self.max_page_num+1,self.num_pages+1)
        return range(self.current_page-part,self.current_page+part+1)

    def page_str(self,base_url):
        page_list = []
        first_page = '<li><a href="%s?p=1">首页</a></li>'%base_url
        page_list.append(first_page)
        if self.current_page == 1:
            prev_page = '<li><a href="javascript:void(0);" class="hide">上一页</a>'
        else:
            prev_page = '<li><a href="%s?p=%s">上一页</a></li>'%(base_url,self.current_page-1)
        page_list.append(prev_page)
        for i in self.page_num_range():
            if i == self.current_page:
                temp = '<li class="active"><a href="%s?p=%s">%s</a></li>' % (base_url,i, i)
            else:
                temp = '<li><a href="%s?p=%s">%s</a></li>'%(base_url,i,i)
            page_list.append(temp)
        if self.current_page == self.num_pages:
            next_page = '<li><a href="javascript:void(0);" class="hide">下一页</a></li>'
        else:
            next_page = '<li><a href="%s?p=%s">下一页</a></li>' % (base_url,self.current_page + 1)
        page_list.append(next_page)
        last_page = '<li><a href="%s?p=%s">尾页</a></li>'%(base_url,self.num_pages)
        page_list.append(last_page)
        return ''.join(page_list)