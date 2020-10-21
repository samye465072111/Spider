# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import openpyxl
import time


class TtPipeline(object):
    def __init__(self):
        self.this_time = str(time.time())
        self.wb = openpyxl.Workbook('./result_'+self.this_time+'.xlsx')
        self.ws = self.wb.active
        self.wb.save('./result_'+self.this_time+'.xlsx')
        self.wb = openpyxl.load_workbook('./result_'+self.this_time+'.xlsx')
        self.ws = self.wb.active


    def process_item(self, item, spider):
        self.ws.append([item['title'],item['new_url'],item['behot_time']])

        return item

    def close_spider(self, spider):
        self.wb.save('./result_'+self.this_time+'.xlsx')
        self.wb.close()