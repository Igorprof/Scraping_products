# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class ProductScraperPipeline:
    def open_spider(self, spider):
        self.connection = sqlite3.connect('db.db')
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS products(
                title TEXT,
                price TEXT,
                description TEXT,
                image TEXT
            )
        """)

        self.connection.commit()

    def process_item(self, item, spider):
        self.cursor.execute("""
            INSERT INTO products(
                title,
                price,
                description,
                image
            ) VALUES (
                ?,
                ?,
                ?,
                ?
            )
        """, (item.get('title'), item.get('price'), item.get('description'), item.get('image')))

        self.connection.commit()

    def close_spider(self, spider):
        self.connection.close()