from crawler import RecipeCrawler

r = RecipeCrawler('data.bin')

with open('data.json', 'w') as f:
    f.write(r.data_json)
