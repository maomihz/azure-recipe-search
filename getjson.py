from crawler import RecipeCrawler

r = RecipeCrawler('data.bin')

print("Visited:", len(r.data['recipes']))
print("Recipes:", len(r.data['recipes_data']))

with open('data.json', 'w') as f:
    f.write(r.data_json)
