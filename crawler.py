import pickle
import requests
from allrecipes import AllRecipes
import re
import json

re_allrecipes = re.compile(r'https?:\/\/(?:www[.])?allrecipes[.]com\/recipe\/([0-9]+)')

class RecipeCrawler:
    # Default data
    data = {
        'urls': {},
        'recipes': {}
    }

    def __init__(self, file):
        self.file = file
        self.load_data()

    # Dump data and load data from file
    def dump_data(self):
        with open(self.file, 'wb') as f:
            pickle.dump(self.data, f)

    def load_data(self):
        try:
            with open(self.file, 'rb') as f:
                data = pickle.load(f)
                self.data = data
        except FileNotFoundError as e:
            open(self.file, 'w').close();
        except TypeError as e:
            pass
    
    @property
    def data_json(self):
        return json.dumps(self.data, indent=2)

    def add_data(self, url):
        if url in self.data['urls']:
            return
        r = requests.get(url)

        # Process redirects
        for h in r.history + [r]:
            self.__process_response(h)
        
    def __process_response(self, response):
        data = {
            'status_code': response.status_code
        }
        print(response.url)
        
        # If success, I need to fetch the actual recipe data
        if response.status_code == requests.codes.ok:
            try:
                recipe_id = re_allrecipes.search(response.url).group(1)
                recipe = AllRecipes.get(response.url)
            except:
                recipe = None
            data['recipe'] = recipe_id
            self.data['recipes'][recipe_id] = recipe
        # If redirect, remember the destination
        elif response.is_redirect:
            data['redirect_to'] = response.headers['Location']
        
        # If error, do nothing
        self.data['urls'][response.url] = data
        

