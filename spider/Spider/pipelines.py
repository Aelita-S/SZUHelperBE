# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface


class DjangoPipeline:
    def process_item(self, item, spider):
        item.save()  # 通过Django ORM 保存
        return item
