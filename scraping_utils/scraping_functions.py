import requests
import re
from bs4 import BeautifulSoup, Comment
from text_utils.text_manipulation import time_string_to_minutes, find_first_number, find_raw_ingredient

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

def get_recipe_urls_from_pages(startPage: int, endPage: int) -> set:
    """
    Finds the recipe URLs from the search pages specified.

    Requests the html content of the given pages and scrapes them to obtain a set of recipe URLs.
    
    Args:
        startPage (int): The page to begin URL scraping on
        endPage (int): The page to end URL scraping on

    Returns:
        set: The set of recipe URLs found.
    """

    #set the base URL and initialise an empty recipe URL set
    baseUrl = 'https://www.bbcgoodfood.com'
    recipeUrls = set()

    #for each page to inspect, generate a url and obtain the response with an appropriate request
    for page in range(startPage, endPage + 1):
        url = f'{baseUrl}/search?page={page}'
        response = requests.get(url, headers=headers)

        #print the current page under inspection
        print(f"At page {page} scraping {url}")

        #if the page cannot be loaded correctly, print an error and continue with the next page
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}. Continuing to the next page...")
            break

        #instantiate a new soup object as a html parser over the response received
        soup = BeautifulSoup(response.text, 'html.parser')

        #obtain the recipe cards div on the page and generate a set of anchor tag links
        recipeCards = soup.find('div', class_='layout-md-rail__primary')
        recipeAnchorTags = recipeCards.find_all('a', class_='link d-block')

        #for each anchor tag, obtain its link and add it to the recipe URL set
        for anchorTag in recipeAnchorTags:
            link = f'{baseUrl}{anchorTag['href']}'
            recipeUrls.add(link)

    #return the recipe URLs found
    return recipeUrls 


def get_recipe_details(recipeUrl: str) -> tuple:
    """
    Finds the recipe details from a given URL.

    Requests the html content of the given URL page and scrapes useful information off and processes them.
    
    Args:
        recipeUrl (str): The recipe page URL to scrape from

    Returns:
        tuple | None: The tuple of recipe attributes scraped from the URL or None if the page cannot be reached
        structure:
            - title (str): The title of the recipe.
            - image_link (str): The URL of the recipe image.
            - raw_ingredients (List[str]): List of raw ingredient names.
            - measured_ingredients (List[str]): List of ingredients with measurements.
            - method (List[str]): List of cooking steps.
            - author (str): The author of the recipe.
            - prep_time (int): Preparation time in minutes.
            - cook_time (int): Cooking time in minutes.
            - difficulty_level (str): Difficulty level of the recipe.
            - rating (float): Average rating of the recipe.
            - ratings_count (int): Number of ratings given.
            - calories, fat, saturates, carbs, sugars, fibre, protein, salt (float): Nutritional information.
    """
    #request the URL and obtain the response with an appropriate request
    response = requests.get(recipeUrl)

    #if the page loaded did not load correctly, print an error and return None 
    if response.status_code != 200:
        print("Failed to retrieve recipe page.")
        return None
        
    #create a new soup as a html parser over the html document returned
    soup = BeautifulSoup(response.text, 'html.parser')

    #obtain the title of  the recipe
    title = soup.find('div', class_='post-header__title').get_text(strip=True)

    #obtain the image link
    imageLink = soup.find('div', class_='image__container').find('img', class_='image__img')['src']

    #obtain the list of ingredients and initialise measured and raw ingredient list
    ingredients = soup.find('section', class_='recipe__ingredients').find_all('li')
    measuredIngredients = []
    rawIngredients = []

    #for each ingredient in the document, add it to the measured ingredient list
    for ingredient in ingredients:
        measuredIngredients.append(ingredient.get_text())

        #attempt to find the raw ingredient name in an anchor tag and add it
        anchorTag = ingredient.find('a', class_='link--styled')
        if anchorTag:
            rawIngredients.append(anchorTag.get_text(strip=True).replace(',', ''))

        #otherwise attempt to find the first comment separator and choose the raw ingredient name
        else:
            ingredient_strings = []

            # Iterate through the contents of the <li> tag
            for content in ingredient.contents:
                # Check if the content is a NavigableString (text node)
                if isinstance(content, str) and (content.strip()):
                    ingredient_strings.append(str(content).replace(',','').strip())

            rawIngredients.append(find_raw_ingredient(ingredient_strings))

    #obtain the author of the 
    author = soup.find('div', class_='author-link').get_text(strip=True)

    #extract method steps and intialise an empty method list
    steps = soup.find('section', class_='recipe__method-steps').find_all('p')
    method = []

    #populate the method list with the steps found
    for step in steps:
        method.append(step.get_text(strip=True))

    #obtain the set of prep and cook times and set the times to zero
    timeElements = soup.select('.post-header__cook-and-prep-time time')
    prepTime=0
    cookTime=0

    #reassign the prep and cook times dependent upon their existence
    if (len(timeElements) > 0):
        prepTime = time_string_to_minutes(timeElements[0].get_text(strip=True))
        if (len(timeElements) > 1):
            cookTime = time_string_to_minutes(timeElements[1].get_text(strip=True))

    #obtain the difficulty level of the recipe
    difficultyLevel = soup.find('div', class_='post-header__skill-level').get_text(strip=True)

    #obtain the rating and ratings count parent div
    ratingsDiv = soup.find('div', class_='rating__values')

    #find the rating and ratings count numbers by finding the first numerical value in the string
    rating = find_first_number(ratingsDiv.find('span', class_='sr-only').get_text(strip=True))
    ratingsCount = int(find_first_number(ratingsDiv.find('span', class_='rating__count-text').get_text(strip=True)))

    #obtain the nutrient information parent table
    nutritionalContent = soup.find('table', class_='key-value-blocks').find_all('tr', class_='key-value-blocks__item')
    
    #for each nutritional value, obtain the key and numerical value for that category
    for nutrient in nutritionalContent:
        nutrientType = nutrient.find('td', class_='key-value-blocks__key').get_text(strip=True)
        nutrientValue = find_first_number(nutrient.find('td', class_='key-value-blocks__value').get_text(strip=True))

        #match the value to the correct category for return
        match(nutrientType):
            case "kcal":
                calories = nutrientValue
            case "fat":
                fat = nutrientValue
            case "saturates":
                saturates = nutrientValue
            case "carbs":
                carbs = nutrientValue
            case "sugars":
                sugars = nutrientValue
            case "fibre":
                fibre = nutrientValue
            case "protein":
                protein = nutrientValue
            case "salt":
                salt = nutrientValue

    #return the recipe information as a tuple
    return (title, imageLink, rawIngredients, measuredIngredients, method, author, prepTime, cookTime, difficultyLevel, rating, ratingsCount, calories, fat, saturates, carbs, sugars, fibre, protein, salt)
        
