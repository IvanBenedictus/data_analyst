import scrapy
from bookscrapper.items import BookscrapperItem


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        # CSS Selector: https://www.w3schools.com/cssref/css_selectors.php
        books = response.css("article.product_pod")

        for book in books:
            relative_url = book.css("article.product_pod h3 a::attr(href)").get()

            if "catalogue/" in relative_url:
                book_url = "https://books.toscrape.com/" + relative_url
            else:
                book_url = "https://books.toscrape.com/catalogue/" + relative_url
            yield response.follow(book_url, callback=self.parse_book)

        next_page = response.css("li.next a::attr(href)").get()

        if next_page is not None:
            if "catalogue/" in next_page:
                next_url = "https://books.toscrape.com/" + next_page
            else:
                next_url = "https://books.toscrape.com/catalogue/" + next_page
            yield response.follow(next_url, callback=self.parse)

    def parse_book(self, response):
        # XPath Syntax: https://www.w3schools.com/xml/xpath_syntax.asp
        table_rows = response.css("article.product_page table.table tr")

        book_item = BookscrapperItem()

        book_item["upc"] = table_rows[0].css("td::text").get()
        book_item["title"] = response.css("article.product_page div.product_main h1::text").get()
        book_item["type"] = response.xpath("//ul[@class='breadcrumb']/li[2]/a/text()").get()
        book_item["category"] = response.xpath("//ul[@class='breadcrumb']/li[3]/a/text()").get()
        book_item["availability"] = table_rows[5].css("td::text").get()
        book_item["num_reviews"] = table_rows[6].css("td::text").get()
        book_item["stars"] = response.css("article.product_page div.product_main p.star-rating::attr(class)").get()
        book_item["price"] = response.css("article.product_page div.product_main p::text").get()
        book_item["url"] = response.url

        yield book_item
        