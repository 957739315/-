import url_manager,html_downloader,html_output,html_parser
import time
'''
爬取百度百科 Android 关键词相关词及简介并输出为一个HTML tab网页
Extra module:
BeautifulSoup
'''
class SpiderMain(object):
    def __init__(self):
        self.urls=url_manager.UrlManager()
        self.downloader=html_downloader.HtmlDownloader()
        self.parser=html_parser.HtmlParser()
        self.out_put=html_output.HtmlOutput()

    def craw(self,root_url):
        count=1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                new_url=self.urls.get_new_url()
                print("craw %d : %s"%(count,new_url))
                headers={
                    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0"
                }
                html_content=self.downloader.download(new_url,retry_count=2,headers=headers)
                new_urls,new_data=self.parser.parse(new_url,html_content,"utf-8")
                self.urls.add_new_urls(new_urls)
                self.out_put.collect_data(new_data)
                if count>=30:
                    break
                count+=1
                time.sleep(2)
            except Exception as e:
                print("craw failed!\n"+str(e))
        self.out_put.output_html()

if __name__=="__main__":
    rooturl="http://baike.baidu.com/item/Android"
    objSpider=SpiderMain()
    objSpider.craw(rooturl)