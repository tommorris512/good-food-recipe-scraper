#import the regex library
import re
from typing import List

def find_first_number(text: str) -> float | None:
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


def time_string_to_minutes(text: str) -> int:
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

def contains_brackets(text: str) -> bool:
    """
    Determines if a set of brackets exists in a piece of text.
    
    Args:
        text (str): The string to inspect

    Returns:
        bool: Whether the text contains a set of brackets
    """

    #return whether both bracket characters exist in the string
    return '(' in text and ')' in text


def contains_number(text: str) -> bool:
    """
    Determines if a number exists in a piece of text.

    Uses the find_first_number function to determine if a piece of text contains a numeric value.
    
    Args:
        text (str): The string to inspect

    Returns:
        bool: Whether the text contains a number
    """

    #return whether a number could be found
    return find_first_number(text) != None

def contains_keywords(text: str, keywords: List[str]) -> int:
    """
    Finds the number of defined keywords
    
    Args:
        text (str): The string to inspect

    Returns:
        bool: Whether the text contains a set of brackets
    """

    #set the keyword count to zero, and iterate over each keyword
    keywordCount = 0

    for keyword in keywords:

        #if the keyword exists in the text, increment its counter
        if keyword in text:
            keywordCount += 1

    
    return keywordCount
        
def find_raw_ingredient(texts: List[str]) -> str:
    """
    Approximates a raw ingredient from a detailed, segmented list of text

    Develops a suitability score for each piece of text in the list, and chooses the best one. 
    The score is derived from bracket presence, numerical value presence and keyword count.
    
    Args:
        texts (List[str]): The list of text pieces to inspect

    Returns:
        str: The most suitable piece of text for a raw ingredient
    """

    #define an empty dictionary and a list of keywords to check
    suitability = {}
    keywords = ['tbsp', 'tsp', 'oz', 'lb', 'ml', 'kg', 'cup', 'can', 'tin', 'serve', 'optional', 'defrosted', 'frozen']

    #for each text piece in the list, set the score to the number of keywords found
    for text in texts:
        suitabilityScore = contains_keywords(text, keywords)

        #increment the score if the text contains brackets or a number
        if (contains_brackets(text)):
            suitabilityScore += 1
        
        if (contains_number(text)):
            suitabilityScore += 1

        #add the text to the dictionary with an associated value of its score
        suitability[text] = suitabilityScore

    size = len(suitability.keys())

    if (size == 0):
        return None
    
    #initialise an iterator of the dictionary and get the first key-value pair
    iterator = iter(suitability.items())
    minScoreText, minScore = next(iterator)

    if (size == 1):
        return minScoreText

    #iterate over the remaining key-value pairs, and reassign the minimum if necessary
    for key, value in iterator:
        if (value < minScore):
            minScoreText = key
            minScore = value

    #return the peice of text with the lowest score
    return minScoreText