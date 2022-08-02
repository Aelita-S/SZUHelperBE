import logging
from datetime import datetime
from urllib.parse import urljoin

import scrapy
from scrapy import Request, Selector
from scrapy.http import HtmlResponse

from document.models import Document
from utils.time_utils import loc_tz
from w3lib.html import remove_tags

base_url = 'https://www1.szu.edu.cn/board/'


class DocumentSpider(scrapy.Spider):
    name = 'document'
    allowed_domains = ['www1.szu.edu.cn']
    # start_urls = ['urljoin(base_url, f'mylist.asp?top=100&from={quote(dpm.encode("gb18030"))}') for dpm in
    #               departments.values()']
    start_urls = ['https://www1.szu.edu.cn/board/infolist.asp', ]

    custom_settings = {
        'DOWNLOAD_DELAY': 0.5
    }

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url)

    def parse(self, response: HtmlResponse, **kwargs):
        tr_list = response.xpath('/html/body/table//tr[2]/td/table//tr[3]/td/table//tr[3]/td/table//tr[position()>1]')

        href_list = tr_list.xpath('.//td[4]/a/@href').extract()
        res_id = [x.split('=')[1] for x in href_list]

        category_list = tr_list.xpath('.//td[2]//text()').extract()

        for href, doc_id, category in zip(href_list, res_id, category_list):
            if not Document.objects.filter(doc_id=doc_id).exists():
                doc_url = urljoin(base_url, href)
                yield Request(doc_url, callback=self.parse_doc, meta={'doc_id': doc_id, 'category': category})
                # 通过meta向下级请求传值
            else:
                self.log(f"{doc_id}已存在")

    def parse_doc(self, response, **kwargs):
        from spider.Spider.items import DocumentItem
        item = DocumentItem()

        item['doc_id'] = response.meta['doc_id']
        item['category'] = response.meta['category']

        xpath_selector = response.xpath('/html/body/table//tr[2]/td/table//tr[3]/td/table//tr[2]/td/table')

        item['title'] = xpath_selector.xpath('.//tr[1]/td/font//text()').extract_first()
        item['department'], item['create_time'] = self.parse_dpm_and_create_time(xpath_selector)
        item['content'] = self.parse_content(xpath_selector)
        item['last_update_time'] = self.parse_last_update_time(xpath_selector)

        yield item

    def parse_dpm_and_create_time(self, selector: Selector) -> (str, datetime):
        """解析部门和创建时间"""
        department_and_create_time = selector.xpath(
            './/tr[2]/td/font//text()') \
            .extract_first().split(u'\u3000', maxsplit=1)
        department = department_and_create_time[0]
        create_time = datetime.strptime(department_and_create_time[1], '%Y/%m/%d %H:%M:%S').replace(tzinfo=loc_tz)
        return department, create_time

    def parse_last_update_time(self, selector: Selector) -> datetime:
        """解析最近更新时间"""
        time_selector = selector.xpath('.//tr[5]/td[@align="right"]//text()').re(r'\d+')
        try:
            line = [int(x) for x in time_selector]
            last_update_time = datetime(*line[:6], tzinfo=loc_tz)
            return last_update_time  # 列表解包，时区转换
        except ValueError as e:
            self.log(message=f"Error Value: {time_selector}", level=logging.ERROR)
            raise e

    def parse_content(self, selector: Selector):
        raw_content = selector.xpath('.//tr[3]/td[@height="400"]').get()  # TODO 去除多个换行
        content = remove_tags(text=raw_content, which_ones=('img', ))
        return content


if __name__ == '__main__':
    # start_urls = [urljoin(base_url, f'mylist.asp?top=100&from={quote(dpm.encode("gb18030"))}') for dpm in
    #               departments.values()]
    # print(start_urls)
    # print(datetime.strptime('2020-9-30', '%Y-%m-%d'))
    import re

    s = "（本文最近更新于2020/7/10 18:52:00　累计点击数:193）"
    print(re.findall(r'\d+', s))
