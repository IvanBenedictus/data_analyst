# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscrapperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Strip all whitespaces from string
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()

        # Category & Product Type lowercase
        lowercase_keys = ["type", "category"]
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        # Convert price to float
        price_key = adapter.get("price")
        value = price_key.replace("£", "")
        adapter["price"] = float(value)

        # Availability to integer
        availability_string = adapter.get("availability")
        split_string = availability_string.split("(")
        if len(split_string) < 2:
            adapter["availability"] = 0
        else:
            availability_key = split_string[1].split(" ")
            adapter["availability"] = int(availability_key[0])

        # Convert Review to integer
        num_reviews_key = adapter.get('num_reviews')
        adapter['num_reviews'] = int(num_reviews_key)

        # Convert Star number from text to number
        stars_string = adapter.get('stars')
        split_array = stars_string.split(' ')
        stars_text_value = split_array[1].lower()
        if stars_text_value == "zero":
            adapter['stars'] = 0
        elif stars_text_value == "one":
            adapter['stars'] = 1
        elif stars_text_value == "two":
            adapter['stars'] = 2
        elif stars_text_value == "three":
            adapter['stars'] = 3
        elif stars_text_value == "four":
            adapter['stars'] = 4
        elif stars_text_value == "five":
            adapter['stars'] = 5

        return item
    

import psycopg2

class SaveToPostgreSQLPipeline():
    def __init__(self):
        self.connect = psycopg2.connect(
            host = "localhost",
            dbname = "WebScrapping",
            user = "postgres",
            password = "ivanbenedictus",
            port = 5432
        )
        self.cursor = self.connect.cursor()

        # Create a Table
        create_table = """
        CREATE TABLE IF NOT EXISTS bookspider(
            upc VARCHAR(16), 
            title VARCHAR(255),
            type VARCHAR(255),
            category VARCHAR(255),
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            price DECIMAL,
            url VARCHAR(255),
            CONSTRAINT pk_upc PRIMARY KEY (upc)
        )
        """
        self.cursor.execute(create_table)

    def process_item(self, item, spider):
        data_name = """
        INSERT INTO bookspider(
            upc,
            title,
            type,
            category,
            availability,
            num_reviews,
            stars,
            price,
            url
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        data_values = (
            item["upc"],
            item["title"],
            item["type"],
            item["category"],
            item["availability"],
            item["num_reviews"],
            item["stars"],
            item["price"],
            item["url"]
        )

        self.cursor.execute(data_name, data_values)
        self.connect.commit()

        return item
    
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
        