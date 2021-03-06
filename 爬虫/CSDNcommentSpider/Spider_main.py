from http import cookiejar
from urllib import request
import re
from urllib.parse import urlencode



class CSDNspider(object):
    def __int__(self):
        self.url_login="https://passport.csdn.net/account/login"
        self.url_feedback="http://write.blog.csdn.net/feedback"
        self.opener=self.create_cookie_opener()
        self.opener.addheaders=[
            ("User-Agent","Mozilla/5.0 (Windows NT 10.0; …) Gecko/20100101 Firefox/59.0"),
            ("Host","passport.csdn.net")
        ]

    def create_cookie_opener(self):
        '''
        设置启用Cookie
        :return: 返回一个自定义的opener
        '''
        cookie=cookiejar.CookieJar()
        cookie_process=request.HTTPCookieProcessor(cookie)
        opener=request.build_opener(cookie_process)
        #print("test!\n")
        return opener

    def get_random_webflow_form(self):
        '''
         获取随机流水号，CSDN网站登录时需要随表单提交一个随机登录流水key
        :return: 返回FORM表单流水字典
        '''
        try:
            content=self.opener.open(self.url_login).read().decode("utf-8")
            lt=re.search(re.compile(r'<input name="lt" value="(.*?)" type="hidden"'),content)
            execution=re.search(re.compile(r'<input name="execution" value="(.*?)" type="hidden"'),content)

            '''分组匹配输出时 re 的 group(x) 方法套路要谨防，group(0) 是原始字符串，group(1)、group(2) ……才是第 1、2、……个分组子串'''

            return {'lt':lt.group(1),'execution':execution.group(1),'_eventId':'submit'}
        except Exception as e:
            print("get random webflow form Exception."+str(e))
            return dict()

    def login(self,user_name=None,password=None):
        '''
         登录CSDN账号
        :param user_name:用户名
        :param password:密码
        :return:返回登陆后的JS自动跳转redirect
        '''
        if user_name is None or password is None:
            print("You need use a valied user name and password to login!")
            return None
        post_form=self.get_random_webflow_form()
        post_form["username"]=user_name
        post_form["password"]=password
        # urllib库里面有个urlencode函数，可以把key - value这样的键值对转换成我们想要的格式
        post_data=urlencode(post_form).encode("utf8")
        print(str(post_form))
        try:
            content=self.opener.open(self.url_login,data=post_data).read().decode("utf8")
            redirect=re.search(re.compile(r'var redirect="(.*?)"'),content)
            return redirect.group(1)
        except Exception as e:
            print("login Exception."+str(e))
            return None

    def run_redirect_back(self,redirect=None):
        '''
        CSDN登陆后返回一个自动执行的 JS 跳转函数，执行后才能算登录验证成功
        :param redirect:JS 方法中定义的 redirect 链接
        :return:成功失败
        '''
        if redirect is None:
            print("run_redirect_back_params redirect is None!")
            return False
        self.opener.open(redirect)
        return True

    def get_page_feedback_dict(self,page_index=1):
        '''
        获取CSDN我的博客页面的评论管理页面我文章的评论列表（按照评论页数获取）
        :param page_index:
        :return:{'maxPage'100:, 'dict':[{'article':'xxx', 'url':'xxx', 'commentator':'xxx', 'time':'xxx', 'content':'xxx'}]}
        '''
        content=self.opener.open(self.url_feedback+str(page_index)).read().decode("utf-8")
        print(content)
        max_page = re.search(re.compile(r'<div class="page_nav"><span>.*?共(\d+)页</span>'), content).group(1)
        reg_main = re.compile(
            r"<tr class='altitem'>.*?<a href='(.*?)'.*?>(.*?)</a></td><td><a.*?class='user_name' target=_blank>(.*?)</a></td><td>(.*?)</td>.*?<div class='recon'>(.*?)</div></td></tr>",
            re.S)
        main_items=re.findall(reg_main,content)
        dict_list=list()
        for item in main_items:
            dict_list.append({
                'url':item[0],
                'article':item[1],
                'commentator':item[2],
                'time':item[3],
                'content':item[4]
            })
        return {'maxpage':max_page,'dict':dict_list}

    def run(self,name=None,pwd=None):
        redirect=self.login(name,pwd)
        if self.run_redirect_back(redirect) is False:
            return
        total_feedback=0
        cur_page=1
        max_page=1
        while cur_page<=max_page:
            print("Start get "+str(cur_page)+"page feedback.")
            page_dict=self.get_page_feedback_dict(cur_page)
            total_feedback=total_feedback+len(page_dict['dict'])
            max_page=int(page_dict['maxPage'])
            cur_page=cur_page+1

        print("Finish Total Valid Feedback is: "+str(total_feedback))

if __name__=="__main__":
    CSDNspider().run("95773915@qq.com","&Hxx520Cmr&")


