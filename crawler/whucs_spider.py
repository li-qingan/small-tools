#coding=utf-8
from fileinput import filename
import scrapy
#from scrapy.conf import settings

#settings.overrides['HTTPERROR_ALLOWED_CODES'] = [500] 

class QuotesSpider(scrapy.Spider):

    custom_settings = {
        'HTTPERROR_ALLOWED_CODES': [500],
    }
    name="quotes"
    pageID=195
    pageMax=469
    start_urls = [
	'http://cs.whu.edu.cn/teacherinfo.aspx?id=',
    ]

    def parse(self, response):
        quotes = response.css('div.about ul.about_info')
        for quote in quotes:
            name = quote.css('li::text').getall()

            #self.log(name)
            print(name)
            #with open("staffInfo.txt", 'a') as f:
                #f.write(name)
            #yield {
            #    str(self.pageID): quote.css('li::text').get(),
            #    '正文': quote.css('section/*/text()').getall(),
            #}

        self.pageID=self.pageID+1
        next_page = 'http://cs.whu.edu.cn/teacherinfo.aspx?id='+str(self.pageID)
	
        if self.pageID > self.pageMax:
                return
        try:
            self.log("access " + next_page)
            yield response.follow(next_page, self.parse)
        except:
            self.log("skip " + next_page)
            self.pageID + self.pageID + 1
            next_page = self.start_urls[0][-1:]+str(self.pageID)
            self.log("try " + next_page)
            yield response.follow(next_page+1, self.parse)
            pass
'''
        if next_page is not None :
            self.log("access " + next_page)
            yield response.follow(next_page, self.parse)
            
        else:
            self.log("skip " + next_page)
            self.pageID = self.pageID+1
            next_page = self.start_urls[0][-1:]+str(self.pageID)
 '''      
