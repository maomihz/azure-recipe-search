# CloudFoodies Crawler

Crawl recipes with [hhursev/recipe-scrapers](https://github.com/hhursev/recipe-scrapers).

Right now the crawler crawls data only from https://allrecipes.com. The code does not search for allrecipes URL, so URLs need to be manually specified.

Suppose there is a text file like this, called `input.txt`:

```
https://www.allrecipes.com/recipe/270862/chicken-enchiladas-with-green-chile-sauce-salsa-verde/
https://www.allrecipes.com/recipe/270862/chicken-enchiladas-with-green-chile-sauce-salsa-verde/
https://www.allrecipes.com/recipe/10294/the-best-lemon-bars/
https://www.allrecipes.com/recipe/10294/the-best-lemon-bars/
https://www.allrecipes.com/recipe/270371/banana-cheesecake-with-banana-cream-pie-topping/
https://www.allrecipes.com/recipe/270371/banana-cheesecake-with-banana-cream-pie-topping/
https://www.allrecipes.com/recipe/17066/janets-rich-banana-bread/
https://www.allrecipes.com/recipe/17066/janets-rich-banana-bread/
https://www.allrecipes.com/recipe/229960/shrimp-scampi-with-pasta/
https://www.allrecipes.com/recipe/229960/shrimp-scampi-with-pasta/
https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/
https://www.allrecipes.com/recipe/10813/best-chocolate-chip-cookies/
https://www.allrecipes.com/recipe/214498/sunday-morning-lemon-poppy-seed-pancakes/
https://www.allrecipes.com/recipe/214498/sunday-morning-lemon-poppy-seed-pancakes/
https://www.allrecipes.com/recipe/242352/greek-lemon-chicken-and-potatoes/
https://www.allrecipes.com/recipe/242352/greek-lemon-chicken-and-potatoes/
```

`grep` the recipe ID and feed it to the crawler:

```
$ cat input.txt | grep -o '/recipe/[0-9]*/' | grep -Eo '[0-9]+' | sort | uniq | python main.py
```

## Rate Limit

allrecipes.com has a rate limit that block crawlers. Once rate limit is hit, all requests are rejected with connection reset error. It is tested to be fine at the rate of 3 secs / page.

Once blocked by allrecipes, there seems to be no way to unblock except changing public IP address.

## Data format

Exports data format and internal data format is different. Internally data is stored in a `dict` object, and data dump is in `pickle` format. Run the `getjson.py` to convert internal data into `json` format, and run `export.py` to export data into separate json files.

### Internal Data

```
{
    "urls": {}
    "recipes": {}
    "recipes_data": {}
    "duplicates": {}
}
```

* `urls`: url => UrlObject
* `recipes`: id => RecipeRefObject
* `recipes_data`: title => RecipeObject
* `duplicates`:

#### UrlObject

Stores all visited URLs. Identified by URL string.

```
{
    "status_code": 200
    "redirect_to": "https://www.allrecipes.com/recipe/50121/blushing-snowballs/"
    "recipe": "50000"
}
```

* `status_code`: HTTP status code for the given URL
* `redirect_to`: If status is 301 / 302, the final redirect destination of the url, in full format.
* `recipe`: If status is 200, the recipe reference ID.

#### RecipeRefObject

Recipe reference without the actual recipe data. Identified by unique recipe ID.

```
{
    "title": "recipe title",
    "url": "https://www.allrecipes.com/recipe/50121/blushing-snowballs/",
    "host": "allrecipes.com"
}
```

* `title`: Recipe title
* `url`: Recipe URL
* `host`: Recipe host (recipe provider)

#### RecipeObj
Actual recipe data.

```
{
    "ingredients": [],
    "instructions": "string",
    "total_time": 20
}
```

* `ingredients`: Ingredients array, in descriptive format
* `instructions`: Cooking instructions as a string
* `total_time`: Total cooking time.


### Export Data

Exported data would be placed in the `data/` folder as individual JSONs named "`{ID}.json`". Each object is combined RecipeRefObject and RecipeObj.

```
{
    "ingredients": [],
    "instructions": "string",
    "total_time": 20,
    "title": "recipe title",
    "url": "https://www.allrecipes.com/recipe/50121/blushing-snowballs/",
    "host": "allrecipes.com"
}
```

### Files

* `main.py`: Entry point.
* `getjson.py`: Convert internal data to JSON format.
* `export.py`: Export JSON data into individual files.
* `crawler.py`: Core functionality of the crawler.
* `upgrade_1.py`: Upgrade the database version (no longer useful since it's a one shot upgrade).