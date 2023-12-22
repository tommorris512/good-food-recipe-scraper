import os
from typing import Tuple
from scraping_utils.scraping_functions import getRecipeUrlsFromPages
from csv_utils.csv_functions import writeRecipeUrlsToCsv, writeRecipeDetailsToCsv


def printMenuOptions() -> None:
    """
    Print the menu options for the program.

    Returns:
        None
    """

    #print the options
    print('Choose an option:')
    print('1 - Write recipe URLs to CSV')
    print('2 - Write recipe details to CSV')


def getFilename() -> str:
    """
    Obtain a filename for the program to write CSV data to.

    Return:
        str: The filename inputted
    """

    #set a flag to determine if a filename is appropriate for use
    acceptibleFilename = False

    #while no appropriate filename is provided, obtain a new file name
    while (not acceptibleFilename):
        print('Enter a filename:')
        filename = input()

        #if the file already exists, output a warning and obtain a decision as to whether to overwrite
        if (os.path.exists(filename)):
            print('Warning, file already exists and will be overwritten. Do you wish to proceed (y/n)')

            #set a flag to determine if the overwriting decision response is acceptible
            validResponse = False
            
            #while no valid decision is provided, take an input converted to lower case
            while (not validResponse):
                response = input().lower()

                #overwrite or not dependent on the decision and output an error for an invalid response
                if (response == 'y'):
                    validResponse = True
                    acceptibleFilename = True
                elif (response == 'n'):
                    validResponse = True
                else:
                    print('Invalid input, please choose y or n to confirm')

        #otherwise if the file does not exist, proceed as normal
        else:
            acceptibleFilename = True

    return filename


def getPageNumber() -> int:
    """
    Obtain a valid page number for data scraping range.

    Return:
        int: The valid page number inputted
    """

    #set a flag to determine if the page number inputted is valid
    validInt = False

    #while the input supplied is not valid, obtain a new page number
    while (not validInt):
        pageNumber = input()

        #attempt to cast the input to an integer
        try:
            pageNumber = int(pageNumber)

            #if the page number if greater than zero, set the flag to valid
            if (pageNumber > 0):
                validInt = True

            #otherwise output an error and obtain a new input
            else:
                print(f'Invalid input, number must be greater than zero. Received: {pageNumber}')

        #if the cast fails, output an error and obtain a new input
        except(ValueError):
            print(f'Invalid input, input is not an integer. Received: {pageNumber}')

    return pageNumber
        

def getPageNumbers() -> Tuple[int]:
    """
    Obtain a valid start and end page number respectively.

    Returns:
        Tuple[int]: The start and end page numbers
    """

    #obtain the start page number
    print('Enter a start page number:')
    startPage = getPageNumber()

    #obtain the end page number
    print('Enter an end page number:')
    endPage = getPageNumber()

    return startPage, endPage


def main() -> None:
    """
    Define the main program to execute data scraping.

    This presents the choice of writing a CSV file of recipe URLs or details from a range of pages.
    It prompts for a page range to operate over and a filename to write the CSV data to.

    Returns:
        None
    """

    #output the options and set a flag to determine a valid choice
    printMenuOptions()
    validChoice = False

    # while the choice is not valid, obtain a new choice
    while (not validChoice):
        choice = input()

        #if the choice is 1 or 2, obtain page numbers and filenames and execute the appropriate CSV writing function
        if choice == '1':
            validChoice = True
            startPage, endPage = getPageNumbers()
            filename = getFilename()
            writeRecipeUrlsToCsv(startPage, endPage, filename)
            print(f'Recipe URLs successfully written to {filename}')
        elif choice == '2':
            validChoice = True
            startPage, endPage = getPageNumbers()
            filename = getFilename()

            recipeUrls = getRecipeUrlsFromPages(startPage, endPage)
            writeRecipeDetailsToCsv(recipeUrls, filename)
            print(f'Recipe details successfully written to {filename}')

        #otherwise, output an error and re-output the choice selection
        else:
            print(f'Invalid input, received: {choice}')
            printMenuOptions()      
           

#run the main program
main()