#import the regex library
import re
from typing import List
from ingredient_parser import parse_ingredient

def findFirstNumber(text: str) -> float | None:
    """
    Finds the first number in a string of text.

    Searches for the first occurence of an integer or floating point value in a string of text. 
    It is ignorant of spacing.
    
    Args:
        text (str): The string to inspect

    Returns:
        float | None: The first numeric value to be found. Returns None if no match is found.
    """

    #define regex patterns for floats and ints
    integerPattern = r'\d+'
    floatPattern = r'\d+\.\d+'

    #combine these to form a general number pattern
    numberPattern = re.compile(f'{floatPattern}|{integerPattern}')

    #search for the first match in the text
    match = numberPattern.search(text)

    #if a match exists, convert to a float and return, otherwise return None
    if match:
        return float(match.group())
    else:
        return None


def timeStringToMinutes(text: str) -> int:
    """
    Finds the total number of minutes from a formatted hours and minutes piece of text.

    Searches for occurences of hour values and minute values, multiplying and summing to derive the total number of minutes.
    
    Args:
        text (str): The string to inspect

    Returns:
        int: The total number of minutes calculated from the text
    """

    #define regex patterns for numerical hours and minutes values
    hoursPattern = re.compile(r'(\d+)\s*hrs?')
    minutesPattern = re.compile(r'(\d+)\s*mins?')

    #intialise counters for the hours and minutes
    totalHours = 0
    totalMinutes = 0

    #find the first match for an hours value and add it to the counter
    hoursMatch = hoursPattern.search(text)
    if hoursMatch:
        totalHours += int(hoursMatch.group(1))

    #find the first match for an minutes value and add it to the counter
    minutesMatch = minutesPattern.search(text)
    if minutesMatch:
        totalMinutes += int(minutesMatch.group(1))

    #add the additional minutes from the hours counter found in the text and return
    totalMinutes += totalHours * 60

    return totalMinutes
        
def findRawIngredient(ingredientText: str) -> str:
    """
    Approximates a raw ingredient from a measured ingredient piece of text.

    Calls the ingredient_parser NLP to find and return the most suitable ingredient name.
    
    Args:
        ingredientText (str): The measured ingredient string to inspect

    Returns:
        str | None: The raw ingredient name, or None if no name could be found
    """
    try:
        return parse_ingredient(ingredientText).name.text
    except(Exception):
        return None
