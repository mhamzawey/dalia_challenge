import scrapy
import string

import datetime

#http://berghain.de/events/
class Berghain(scrapy.Spider):
    name = "berghain"

    BASE_URL ="http://berghain.de"

    urls = [BASE_URL+"/events/"]

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def clean_text(self,text):
        printable = set(string.printable)
        return ''.join(filter(lambda x: x in printable, text))

    def parse(self, response):
        list = []
        for type in response.css(".navi_level3_extra ::attr(class)"):
            if type.extract() != "navi_level3_extra":
                _class = ".col_teaser_{}"
                for event in response.css(_class.format(type.extract())):
                    dict = {}
                    date =[x.strip() for x in event.css("."+type.extract()+" ::attr(title)").extract_first().split(':')][0]
                    title = [x.strip() for x in event.css("."+type.extract()+" ::attr(title)").extract_first().split(':')][1]
                    start = datetime.datetime.strptime(date, '%a %d %B %Y').strftime('%d/%m/%y')
                    end = datetime.datetime.strptime(date, '%a %d %B %Y').strftime('%d/%m/%y')
                    category = response.css("."+type.extract() +"::text").extract_first()
                    href = self.BASE_URL + event.css("."+type.extract()+" ::attr(href)").extract_first()
                    desc = event.css("."+type.extract()+"_color span::text").extract()[1]
                    dict['title'] = self.clean_text(title)
                    dict['start_date'] = start
                    dict['end_date'] = end
                    dict['category'] = category
                    dict['description'] = self.clean_text(desc)
                    dict['link'] = href
                    list.append(dict)


        for item in list:
             yield item

