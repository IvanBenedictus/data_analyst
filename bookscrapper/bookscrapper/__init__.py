## Scrapy Instructions

# Initialization
# 1. Start a scrappy project using "scrapy startproject project_name" command
# 2. Create a spider file in spiders folder using "cd spiders -> scrapy genspider spider_name website_url" command

# Settings Spider
# 1. In scrapy.cfg add "shell = ipython in [settings]"
# 2. In items.py add you data name under "class BookscrapperItem(scrapy.item)"
# 3. In pipelines.py create your data pipeline and add the path to settings.py "ITEM_PIPELINES"
# 3a. class BookscrapperPipeline() - to clean and extract your data
# 3b. class SaveToPostgreSQLPipeline() - to save data inside a database
# 4. In settings.py add ITEM_PIPELINES for adding pipeline and add FEEDS to save with with csv or json format

# Spider Data
# 1. Select you spidername and domain to scrape
# 2. Identify which data you want to scrape and how to get the data using CSS Selector & XPath Syntax
# 3. Open scrapy shell to try your code and look the output using "scrapy shell" command
# 3a. Fetch the url for scrappy shell using "fetch('url')" command
# 4. Exit scrapy shell using "exit" command and add your command to parse function

# Running Command
# 1. Run your project using "scrapy crawl spider_name" command
# 1a. Use "scrapy crawl spider_name -O file_name.json" to save file in json (overwrite)
# 1b. Use "scrapy crawl spider_name -O file_name.csv" to save file in csv (overwrite)
# 1c. Use "scrapy crawl spider_name -o file_name.json" to append file in json (append)
# 1d. Use "scrapy crawl spider_name" if you have setting your save in FEEDS on setting.py