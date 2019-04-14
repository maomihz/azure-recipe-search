import pickle
import requests
from recipe_scrapers import scrape_me
import re
import json

re_allrecipes = re.compile(r'https?:\/\/(?:www[.])?allrecipes[.]com\/recipe\/([0-9]+)')

UA = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:53.0) Gecko/20100101 Firefox/53.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393'
]

class RecipeCrawler:
    # Default data
    data = {
        'urls': {},
        'recipes': {},
        'recipes_data': {},
        'duplicates': {}
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
            return False
        r = requests.get(url, headers={
            'User-Agent': UA[0]
        })

        # Process redirects
        for h in r.history + [r]:
            # Pass the destination url
            self.__process_response(h, r.url)
        return True
        

    def __process_response(self, response, destination = None):
        url_data = dict(status_code=response.status_code)
        print(response.url)
        
        # If success, I need to fetch the actual recipe data
        if response.status_code == requests.codes.ok:
            try:
                recipe_id = re_allrecipes.search(response.url).group(1)
                recipe = scrape_me(response.url)
            except:
                recipe = None
            url_data['recipe'] = recipe_id

            # Add the recipe data
            title = recipe.title()
            host = recipe.host()

            # Construct data
            recipe_index = dict(
                url=response.url,
                host=host,
                title=title
            )
            recipe_data = dict(
                ingredients=recipe.ingredients(),
                instructions=recipe.instructions(),
                total_time=recipe.total_time()
            )

            self.data['recipes'][recipe_id] = recipe_index

            if title not in self.data['recipes_data']:
                self.data['recipes_data'][title] = recipe_data
            # Check for duplicate item
            elif (self.data['recipes_data'][title]['instructions'] != recipe.instructions()):
                print("Duplicate Item!")
                self.data['duplicates'][recipe_id] = recipe_index
                self.data['duplicates'][recipe_id].update(recipe_data)

        # If redirect, remember the destination
        elif response.is_redirect:
            url_data['redirect_to'] = destination
        
        # If error, do nothing
        self.data['urls'][response.url] = url_data
        

