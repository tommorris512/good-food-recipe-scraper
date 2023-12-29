# BBC Good Food Recipe Scraper

This project aims to facilitate the retrieval of recipe URLs and details from the recipes available at the BBC Good Food website.
This project utilises the BeautifulSoup module to extract relevant data attributes from the HTML contents of both the search page and individual recipe pages available on the site.

## Recipe URL Extraction
The URL extraction utility allows a range of search result pages to be visited on the BBC Good Food site, and each recipe link from this page range to be extracted and written to a specified CSV file.
This takes the form of a single column CSV file, that can be utilised for traversal by more specific web scraping utilities, or be read in for recipe detail extraction using the functions provided in the included `csv_utils` module.

## Recipe Detail Extraction
The recipe details extraction utility allows each recipe included over a range of search result pages on the BBC Good Food site's details to be extracted.
This takes the form of a CSV file with the following fields:
 - Title: Title of the recipe
 - Image Link: A URL for the associated recipe image
 - Raw Ingredients: An array of the ingredients used in the recipe
 - Measured Ingredients: A more detailed array of ingredients, including quantities needed for the recipe
 - Method: An array of steps that precisely describe how to create the dish in the recipe
 - Author: The author of the recipe (according to BBC Good Food)
 - Prep Time: The time in minutes the recipe takes to prepare
 - Cook Time: The time in minutes the recipe takes to cook
 - Difficulty Level: A qualitative measure of how difficult the recipe is to recreate
 - Rating: A float from 0 to 5 for the mean average score the recipe received on the BBC Good Food website
 - Ratings Count: The number of ratings the recipe receieved on the BBC Good Food website
 - Calories: The number of calories (kcal) the recipe contains
 - Fat: The quantity of fat in grams the recipe contains
 - Saturates: The quantity of saturates in grams the recipe contains
 - Carbs: The quantity of carbohydrates in grams the recipe contains
 - Sugar: The quantity of sugar in grams the recipe contains
 - Fibre: The quantity of fibre in grams the recipe contains
 - Protein: The quantity of protein in grams the recipe contains
 - Salt: The quantity of salt in grams the recipe contains

This utility is useful for building a reliable recipe dataset of a given size, particularly for filtering recipes by nutritional content, creation time, rating, etc.

## Repository Structure
Additional functions for facilitating the web scraping correctly are contained within additional module directory. These include:
 - `csv_utils`: A collection of utilities for reading from and writing to specified CSV files
 - `text_manipulation`: A collection of utilities for extracting relevant information from more generic text fields
 - `scraping_utils`: A collection of utilities for obtaining the relevant data fields from the HTML content retrieved

## Usage
Clone the repository, (including utility directories, such as `csv_utils`)

Ensure all required modules and dependencies are installed that are not within the standard python library. This includes:
 - requests _(for obtaining the HTML content)_
 - bs4 _(for data extraction from HTML content)_
 - ingredient-parser-nlp _(for raw ingredient name extraction from the HTML content)_
 - averaged_perceptron_tagger from nltk _(for utilising the NLP module correctly)_

This can be achieved by executing the included `setup.py` file.

Once all modules are installed, simply run the included `main.py` file.