# -*- coding: utf-8 -*-
import scrapy
from datetime import datetime

class BeikeSpider(scrapy.Spider):
    name = "beike"
    allowed_domains = ["ke.com"]
    start_urls = []
    url = 'https://sh.ke.com/ershoufang/'
    for i in range(1,101):
        start_urls.append(url +"pg" + str(i) + '/')
    def parse(self, response):
        li_list = response.xpath("//div[@class='leftContent']//ul[@class='sellListContent']//li[@class='clear']")
        for li in li_list:
            item = {}
            item['title'] = li.xpath(".//div[@class='title']/a/text()").extract()[0]
            detailed_url = li.xpath(".//div[@class='title']/a/@href").extract_first()
            item['address'] = {}
            item['address']['position'] = li.xpath(".//div[@class='address']/div[@class='flood']//a/text()").extract()[0]
            item['address']['houseInfo'] = li.xpath(".//div[@class='address']/div[@class='houseInfo']//text()").extract()[1]
            item['tag'] = li.xpath(".//div[@class='address']/div[@class='tag']//text()").extract()
            item['priceInfo'] = {}
            item['priceInfo']['totalPrice'] = li.xpath(".//div[@class='priceInfo']/div[@class='totalPrice']/span/text()").extract()[0]
            item['priceInfo']['unitPrice'] = li.xpath(".//div[@class='priceInfo']/div[@class='unitPrice']/span/text()").extract()[0]
            yield scrapy.Request(
                url= detailed_url,
                callback=self.detailed_info_parser,
                meta={"item":item}
            )
    def detailed_info_parser(self,response):
        item = response.meta['item']
        detail_info = {}
        pic_list = response.xpath("//div[@class='thumbnail']/ul//li")
        picture = []
        detail_info['picture'] = picture
        for pic in pic_list:
            picture.append(pic.xpath("./@data-src").extract_first())
        base_info = response.xpath("//div[@class='m-content']/div[@class='box-l']/div[@id='introduction']//div[@class='introContent']/div[@class='base']")
        base_li = base_info.xpath(".//div[@class='content']/ul//li")
        map_chinese_to_english = {
            "房屋户型":"house_type",
            "所在楼层":"floor",
            "建筑面积":"area",
            "户型结构":"family_structure",
            "建筑类型":"building_type",
            "房屋朝向":"orientation",
            "建筑结构":"building_structure",
            "装修情况":"decoration",
            "梯户比例":"rate_of_elevator_family",
            "配备电梯":"spare_elevator",
            "产权年限":"period_int",
            "挂牌时间":"listing_time",
            "交易权属":"trading_ownership",
            "上次交易":"last_transaction",
            "房屋用途":"usage_of_house",
            "房屋年限":"year_of_house",
            "产权所属":"property_right",
            "抵押信息":"mortgate_info",
            "房本备件":"house_license"
        }
        basic_properity = {}
        for li in base_li:
            name = li.xpath(".//text()").extract()[0]
            if name in map_chinese_to_english.keys():
                name = map_chinese_to_english[name]
            if name == "listing_time":
                temp_time = li.xpath(".//text()").extract()[1]
                temp_time = datetime.strptime(temp_time, "%Y年%m月%d日").isoformat()
                basic_properity[name] = temp_time
            else:
                basic_properity[name] = li.xpath(".//text()").extract()[1]
        detail_info['basic_properity'] = basic_properity
        property_li =response.xpath("//div[@class='m-content']/div[@class='box-l']/div[@id='introduction']//div[@class='introContent']/div[@class='transaction']/div[@class='content']/ul//li")
        property_info = {}
        for li in property_li:
            name = li.xpath(".//text()").extract()[0]
            if name in map_chinese_to_english.keys():
                name = map_chinese_to_english[name]
            temp = li.xpath(".//text()").extract()[1]
            temp = temp.replace("\n",'')
            temp = temp.replace(" ",'')
            property_info[name] = temp
        detail_info['transaction_properity'] = property_info
        item['detail_info'] = detail_info
        yield item






