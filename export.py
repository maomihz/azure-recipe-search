# Export data into individual JSON files
from crawler import RecipeCrawler
import os
from os.path import join, dirname
from json import dumps


if __name__ == '__main__':
    r = RecipeCrawler()
    exports = dict()
    exports_dir = join(dirname(__file__), 'data')
    os.makedirs(exports_dir, exist_ok=True)

    for recipe_id, recipe in r.recipes.items():
        title = recipe['title']
        
        if title not in exports:
            recipe_data = r.recipes_data[title]
            recipe_data.update(recipe)
            recipe_data['id'] = recipe_id
            exports[title] = recipe_data
    
    for recipe in exports.values():
        filename = join(exports_dir, '{}.json'.format(recipe['id']))
        with open(filename, 'w') as f:
            f.write(dumps(recipe, indent=2))
    

