import scrapy


class QuotesSpider(scrapy.Spider):
    name="quotes"
    pageID=283
    pageMax=307
    start_urls = [
       'https://m.aixdzs.com/read/25068/p'+str(pageID)+'.html',
    ]

    def parse(self, response):
        
        for quote in response.css('body div.page-d article.page-content'):
            yield {
                str(self.pageID): quote.xpath('h3/text()').get(),
                '正文': quote.xpath('section/*/text()').getall(),
            }

        self.pageID=self.pageID+1
        next_page = 'https://m.aixdzs.com/read/25068/p'+str(self.pageID)+'.html'
        if self.pageID > self.pageMax:
            pass
        elif next_page is not None :
            self.log("access " + next_page)
            yield response.follow(next_page, self.parse)
            
        else:
            self.log("skip " + next_page)
            self.pageID = self.pageID+1
            next_page = self.start_urls[0][-1:]+str(self.pageID)
        