from crawler import RecipeCrawler
from time import sleep

r = RecipeCrawler('data.bin')

while True:
    try:
        i = input()
    except:
        break
    url = "https://www.allrecipes.com/recipe/" + str(i)
    if r.add_data(url):
        r.dump_data()
        sleep(2)