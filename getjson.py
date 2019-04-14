from crawler import RecipeCrawler

r = RecipeCrawler('output.data')

with open('data.json', 'w') as f:
    f.write(r.data_json)
