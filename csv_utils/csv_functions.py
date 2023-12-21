#import the necessary modules
import csv
from typing import List
from scraping_utils.scraping_functions import get_recipe_urls_from_pages, get_recipe_details


def read_recipe_urls_from_csv(filename: str) -> List[str]:
    """
    Reads the recipe urls from a given csv file.
    
    Args:
        filename (str): The csv file to extra the urls from

    Returns:
        List[str]: The list of urls stored in the file
    """

    #initialise an empty url list and attempt to open the file in read mode
    recipeUrls = []

    try:
        with open(filename, mode='r') as file:
            #set a new dictionary reader and add each url to the list
            reader = csv.DictReader(file)

            for row in reader:
                recipeUrls.append(str(row['Recipe Urls']))

    #if an error is thrown, print the error to stdout
    except Exception as e:
        print(e)

    #close the file and return the url list
    finally:
        file.close()

    return recipeUrls


def read_recipe_details_from_csv(filename: str) -> List[dict]:
    """
    Reads the recipe details of recipes from a given csv file.
    
    Args:
        filename (str): The csv file to extra the recipes' details from

    Returns:
        List[dict]: The list of dictionaries for each recipe in the file
    """

    #initialise an empty recipe details list and attempt to open the file in read mode
    recipeDetails = []

    try:
        with open(filename, mode='r') as file:
            #set a new dictionary reader and add each recipe as a dictionary to the list
            reader = csv.DictReader(file)

            for row in reader:
                recipeDetails.append(row)

    #if an error is thrown, print the error to stdout
    except Exception as e:
        print(e)

    #close the file and return the recipe details list
    finally:
        file.close()

    return recipeDetails


def write_recipe_urls_to_csv(startPage: int, endPage: int, filename: str) -> None:
    """
    Writes the recipe urls from a range of pages to a specified csv file.

    Find the urls from each page using the get_recipe_urls_from_pages function and writes each to the file.
    
    Args:
        startPage (int): The page to begin url scraping on
        endPage (int): The page to end url scraping on
        filename (str): The csv file to write recipe urls to

    Returns:
        None
    """

    #obtain the urls from the specified pages and output a message that file writing has begun
    recipeUrls = get_recipe_urls_from_pages(startPage, endPage)
    print(f'Writing urls to file {filename}')

    #attempt to open the specified file in write mode and create a new csv writer
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            #write a header followed by all the urls found
            writer.writerow(['Recipe Urls'])

            for url in recipeUrls:
                writer.writerow([url])

    #if an error is thrown, print the error to stdout 
    except Exception as e:
        print(e)

    #close the file being written to
    finally:
        file.close()


def write_recipe_details_to_csv(recipeUrls: List[str], filename: str) -> None:
    """
    Writes the recipe details from a list of urls to a specified csv file.

    Find the details from each recipe page using the get_recipe_details function and writes each to the file.
    
    Args:
        recipeUrls (List[str]): The list of recipe page urls to scrape details from
        filename (str): The csv file to write recipe details to

    Returns:
        None
    """

    #attempt to open the specified file in write mode and create a new csv writer
    try:
        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)

            #write a header followed by all details found for each recipe
            writer.writerow(['Title', 'Image Link', 'Raw Ingredients', 'Measured Ingredients', 'Method', 'Author', 'Prep Time', 'Cook Time', 'Difficulty Level', 'Rating', 'Ratings Count', 'Calories', 'Fat', 'Saturates', 'Carbs', 'Sugars', 'Fibre', 'Protein', 'Salt'])

            for url in recipeUrls:
                print(f"Inpsecting url {url}")

                details = get_recipe_details(url)
                
                if details:
                    writer.writerow(details)

    #if an error is thrown, print the error to stdout 
    except Exception as e:
        print(e)

    #close the file being written to
    finally:        
        file.close()