from crawler import RecipeCrawler
from time import sleep

r = RecipeCrawler('output.data')
for i in range(50000, 50100):
    url = "https://www.allrecipes.com/recipe/" + str(i)
    r.add_data(url)
    r.dump_data()
    sleep(5)