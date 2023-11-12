# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item prices with a single interface
from itemadapter import ItemAdapter


class BeastscrapperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Strip all whitespaces from string
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()

        # Propercase Product Name
        proper_case = adapter.get("product")
        adapter["product"] = proper_case.title()

        # Convert price to float
        price_key = adapter.get("price")
        value = price_key.strip()
        value = value.replace(",", "").replace(".", "").replace("Rp", "").replace("IDR", "")
        adapter["price"] = int(value)

        # Convert item to float
        int_values = ["reviews", "num_reviews"]
        for int_value in int_values:
            value = adapter.get(int_value)
            adapter[int_value] = float(value)

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
        CREATE TABLE IF NOT EXISTS beastspider(
            product VARCHAR(255), 
            price INTEGER,
            description VARCHAR(255),
            reviews FLOAT,
            num_reviews FLOAT,
            url VARCHAR(255),
            CONSTRAINT pk_product PRIMARY KEY (product)
        )
        """
        self.cursor.execute(create_table)

    def process_item(self, item, spider):
        data_name = """
        INSERT INTO beastspider(
            product,
            price,
            description,
            reviews,
            num_reviews,
            url
        ) VALUES (%s, %s, %s, %s, %s, %s)
        """
        data_values = (
            item["product"],
            item["price"],
            item["description"],
            item["reviews"],
            item["num_reviews"],
            item["url"]
        )

        self.cursor.execute(data_name, data_values)
        self.connect.commit()

        return item
    
    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
