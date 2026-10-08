# scraper/external_links_spider.py
import scrapy
from urllib.parse import urlparse
import yaml

class ExternalLinksSpider(scrapy.Spider):
    name = "external_links"
    custom_settings = {
        "ROBOTSTXT_OBEY": True,
        "DOWNLOAD_DELAY": 0.2,
        "LOG_LEVEL": "INFO",
    }

    def start_requests(self):
        cfg = yaml.safe_load(open("config.yaml"))
        self.base = cfg["site"]["base_url"]
        self.exclude = set(cfg["site"]["exclude_domains"])
        yield scrapy.Request(self.base, self.parse)

    def parse(self, response):
        # 현재 페이지에 있는 모든 <a href=""> 를 검사
        for href in response.css("a::attr(href)").getall():
            if not href:
                continue
            url = response.urljoin(href)
            domain = urlparse(url).netloc
            # 내부·제외 도메인은 스킵
            if any(domain.endswith(d) for d in self.exclude):
                continue
            # 외부 링크이면 결과에 저장
            yield {"url": url, "source": response.url}

        # 내부 페이지(같은 도메인)도 재귀해서 탐색
        for href in response.css("a::attr(href)").getall():
            next_url = response.urljoin(href)
            if urlparse(next_url).netloc == urlparse(self.base).netloc:
                yield response.follow(next_url, self.parse)
