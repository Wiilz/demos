# -*- coding: utf-8 -*-
import json
import re
from urllib.parse import urljoin

import scrapy
from scrapy import Request

from bt.items import BtItem


class BtspiderSpider(scrapy.Spider):
    name = 'btspider'
    allowed_domains = ['bturl.so']
    bt_host = 'https://www.bturl.so'
    pages = []
    start_urls = ['https://www.bturl.so/0ECDD0BBDBEC26B1457134D5FBAE37111645C28F.html', 'https://www.bturl.so/25A3E8FA1F48670402AA9B45102CC238C5E9CEFC.html',
                  'https://www.bturl.so/10F3D8ECEFC07A696C3C3069FC929A73D3B54001.html', 'https://www.bturl.so/9BFF34114D6BC20C4395E6C0408577F74D6CA771.html']

    def parse(self, response):
        """抓取详情页"""
        print(response.url)
        item = BtItem()
        name_cfmail = response.xpath('//h1[@class="T1"]/a/@data-cfemail').extract()
        name = ''
        if name_cfmail:
            name = ''.join([self.decode(x) for x in name_cfmail])
        item['source_name'] = name + (response.xpath('//div[@class="main"]/h1/text()').extract_first() or '').strip()
        source_infos = response.xpath('//dl[@class="BotInfo"]/p')
        # ='//dl[@class="BotInfo"]/p/text()'
        # data = '文件大小: 1.9 GB' >, < Selec
        item['source_size'] = source_infos.re("文件.*?(\d[\d\w\.\s]*)", re.S)[0].strip()
        item['create_time'] = source_infos.re("日期.*?(\d[\d\w\.\s-]*)", re.S)[0].strip()
        item['source_hot'] = source_infos.re("热度.*?(\d[\d\w\.\s-]*)", re.S)[0].strip()
        item['source_link'] = source_infos.re('(magnet.*?)\"')[0].strip()
        item['old_link'] = response.url[-100:]
        source_list = response.xpath('//ol[@class="flist"]/li')
        info_temp = []
        for source in source_list:
            cfmail_temp_name = source.xpath('a/@data-cfemail').extract()
            temp_name = ''
            if cfmail_temp_name:
                temp_name = ''.join([self.decode(x) for x in cfmail_temp_name])
            temp = {
                'name': (temp_name + (source.xpath('text()').extract_first() or '')).strip(),
                'size': (source.xpath('span/text()').extract_first().strip()) or ''.strip()
            }
            info_temp.append(temp)

        item['source_list'] = json.dumps(info_temp)
        if not item['source_name']:
            item['source_name'] = info_temp[0].get('name')
        yield item
        hot_boxs = response.xpath('//div[@class="hotkbox"]/a/@href')
        for hot_box in hot_boxs:
            links = hot_box.extract()
            if links:
                full_link = urljoin(self.bt_host, links)
                yield Request(url=full_link, callback=self.parse_list)

    def parse_list(self, response):
        """搜索列表页"""
        result_list = response.xpath('//ul[@class="mlist"]/li')
        for result in result_list:
            href = result.xpath('h3/a/@href').extract_first()
            full_url = urljoin(self.bt_host, href)
            yield Request(url=full_url, callback=self.parse)
        pages = response.xpath('//a[@class="flag_pg"]/@href').extract()
        if pages:
            next_page = pages[-1]
            if next_page not in self.pages:
                self.pages.append(next_page)
                full_next_page = urljoin(self.bt_host, next_page)
                yield Request(url=full_next_page, callback=self.parse_list)

    @staticmethod
    def decode(cfemail):
        enc = bytes.fromhex(cfemail)
        return bytes([c^enc[0] for c in enc[1:]]).decode('utf8')


