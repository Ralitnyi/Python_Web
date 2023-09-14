from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())

    # Запуск спайдера QuotesSpider
    process.crawl("quotes")

    # Запуск спайдера AuthorsSpider
    process.crawl("authors")

    # Запуск всіх спайдерів, які ви визначили в налаштуваннях Scrapy
    # process.crawl("spider_name")

    # python main.py quotes authors or python main.py
    process.start()
