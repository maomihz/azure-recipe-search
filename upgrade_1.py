from crawler import RecipeCrawler

r = RecipeCrawler('data.bin')


r.data['titles'] = {}
r.data['recipes_data'] = {}
r.data['duplicates'] = {}

recipes = r.data['recipes']
recipes_data = r.data['recipes_data']

for recipe_id in recipes.keys():
    recipe = recipes[recipe_id]
    
    recipe_title = recipe.pop('title')
    recipe_url = recipe.pop('url')
    recipe_host = recipe.pop('host', 'allrecipes.com')

    recipes_data[recipe_title] = recipe
    recipes[recipe_id] = {
        'title': recipe_title,
        'url': recipe_url,
        'host': recipe_host
    }


r.dump_data()
with open('data.json', 'w') as f:
    f.write(r.data_json)