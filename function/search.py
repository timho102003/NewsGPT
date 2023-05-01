import time
from typing import List, Tuple, Union

import feedparser
import nltk
from newspaper import Article, Config
from pygooglenews import GoogleNews
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

nltk.download("punkt")


class SearchEngine(object):
    def __init__(self, lang="en", country="US"):
        self.engine = GoogleNews(lang=lang, country=country)
        # chrome_options = Options()
        # chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        # chrome_options.add_argument("--disable-notifications")
        # chrome_options.add_argument("--disable-popup-blocking")
        # chrome_options.add_argument("--disable-extensions")
        # chrome_options.add_argument("--headless")
        # self.driver = webdriver.Chrome(options=chrome_options)
        # self.driver.set_page_load_timeout(30)  # Set the page load timeout to 30 seconds
        self._USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self._article_config = Config()
        self._article_config.request_timeout = 20
        self._article_config.browser_user_agent = self._USER_AGENT

    def search(self, keys: str = "", when: str = "1d") -> Tuple[List, List]:
        src_response = self.engine.search(keys, when=when)
        titles, metadatas = [], []
        for t in src_response["entries"]:
            titles.append(t["title"].split(" - ")[0])
            metadatas.append([t["source"]["title"], t["published"], t["link"]])

        return titles, metadatas

    def fetch(self, rss_feed: str = "") -> Union[dict, str]:
        start = time.time()
        news_feed = feedparser.parse(rss_feed)
        # self.driver.get(news_feed["href"])
        # cur_html = self.driver.page_source
        # article = Article(news_feed["href"])
        try:
            # self.driver.get(news_feed["href"])
            # cur_html = self.driver.page_source
            article = Article(news_feed["href"])
            article.download()
            # article.download(input_html=cur_html)
            article.parse()
            # article.nlp()
            end = time.time()
            print(f"Fetch Time: {end -start}")
            return {
                "title": article.title,
                "body": article.text,
                # "summary": article.summary,
                "image": article.top_image,
                "authors": article.authors,
                # "keywords": article.keywords,
                "url": article.url,
            }
        except Exception as e:
            return "[error fetching] : " + str(e)
