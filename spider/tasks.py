import os


class DocumentTask:
    @staticmethod
    def run():
        os.chdir('/app/spider')
        os.system('scrapy crawl document')


if __name__ == '__main__':
    DocumentTask.run()
