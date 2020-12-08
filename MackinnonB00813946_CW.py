# Open the data file, ignore the first two lines and separate the book details into separate strings when a ', ' is detected
bookData = open('bookData.txt', 'r').read().split('\n')[2:]
for detail in range(0, len(bookData)):
    bookData[detail] = bookData[detail].split(', ')

def main():
    # Set default titleText and allow it to be modified in other functions
    global titleText
    titleText = 'The Book Inventory Management Tool'

    headerText()
    # Display program title and menu options
    option = int(input('Please select what you wish to do: ' + \
                       '\n (1) Currently Stocked Books ' + \
                       '\n (2) Average price of Stocked Books ' + \
                       '\n (3) Total Number of Books by Genre ' + \
                       '\n (4) Add Additional Book and Amend Records ' + \
                       '\n (5) Book Availability Check ' + \
                       '\n (6) Ordered List of Current Stock ' + \
                       '\n (7) Chart of Stocked Books by Genre ' + \
                       '\n (8) Exit Program ' + \
                       '\nSection: '))

    # Change titleText and display appropriate function
    if option == 1: 
        titleText = 'Currently Stocked Books'
        currentStock()
    elif option == 2:
        titleText = 'Average price of Stocked Books'
        averagePrice()
    elif option == 3:
        titleText = 'Total Number of Books by Genre'
        numberByGenre()
    elif option == 4:
        titleText = 'Add Additional Book and Amend Records'
        addBook()
    elif option == 5:
        titleText = 'Book Availability Check'
        checkAvailability()
    elif option == 6:
        titleText = 'Ordered List of Current Stock'
        orderedDisplay()
    elif option == 7:
        titleText = 'Chart of Stocked Books by Genre'
        chartByGenre()
    elif option == 8:
        titleText = 'Thank you for using this program'
    else:
        errorHandler()

# Section Functions
def currentStock():
    # Display formatted list of stocked titles
    # Calculate total value of stocked inventory
    # Display number of titles and value of stocked inventory rounded to 2 decimal places
    headerText()

    # Displays a formatted list of currently and/or previously stocked titles
    totalValue = 0
    print('Currently/previously stocked titles:')
    for detail in bookData:
        print('\n ', detail[1], ':', sep='')
        print('  Author:', detail[0])
        print('  Genre:', detail[6])
        print('  Publisher:', detail[3])
        if detail[2] == 'pb':
            print('  Format: Paper Back')
        elif detail[2] == 'hb':
            print('  Format: Hard Back')
        else:
            print('  Format: ', detail[2])
        print('  Cost: £', detail[4], sep='')
        if int(detail[5]) > 0:
            print('  Stock:', detail[5])

            # Calculates the total value of the current inventory
            titleValue = (float(detail[4]) * (float(detail[5])))
            totalValue += titleValue
        else: 
            print('  Stock: Out of Stock')

    # Displays the total number of titles and the total value of the current inventory
    print('\nThe current number of titles available is:', len(bookData))
    print('The total value of the books currently in stock is: £', round(totalValue, 2), sep='')

    sectionEnd()

def averagePrice():
    # Calculate average cost of a single book from the stocked inventory
    # Display average cost rounded to 2 decimal places
    headerText()

    # Calculates the average cost of all stocked titles and displays answer
    totalIndividualCosts = 0
    for detail in bookData:
        if float(detail[5]) > 0:
            totalIndividualCosts += (float(detail[4]))
    averageTitleCost = totalIndividualCosts / len(bookData)
    print('The average price of a title currently in stock is: £', round(averageTitleCost, 2), sep='')

    sectionEnd()

def numberByGenre():
    # Collect a list of all genres present within bookData (Allowing for the addition of new ones)
    # Calculate the number of times each genre is mentioned and add it to a count
    # Display a formated list of the number of times each genre is mentioned
    headerText()

    # Adds all genres stored in bookData to the given list
    genreTypes = []
    for detail in bookData:
        genreTypes.append(detail[6])

    # Calculates the number of times a given genre appears in the bookData and displays answer(s)
    print('There are currently:')
    for genreType in set(genreTypes):
        genreCount = 0
        for detail in bookData:
            if detail[6] == genreType:
                genreCount += 1
        print(' ', genreCount, genreType, 'titles')

    sectionEnd()

def addBook():
    # Get the number of titles the user would like to add
    # Collect the relevent data for each title being added
    # Inform the user when the title(s) have been added
    # Calculate the average BEFORE any additions and AFTER any additions
    # Display the updated number of titles and the difference made to the average cost per title
    headerText()

    # Calculates the average cost of all stocked titles BEFORE any additions
    totalIndividualCosts = 0
    for detail in bookData:
        if float(detail[5]) > 0:
            totalIndividualCosts += (float(detail[4]))
    averageTitleCost_before = totalIndividualCosts / len(bookData)

    # Set the total number of times the code below will run
    amount = int(input('How many titles would you like to add? '))

    # Collect the necessary information for each title and save it to bookData
    for _ in range(amount):
        print('\nPlease provide the following information: ')

        author = input(' Author: ')
        title = input(' Title: ')
        form = input(' Format: ')
        publisher = input(' Publisher: ')
        cost = input(' Cost: ')
        stock = input(' Stock: ')
        genre = input(' Genre: ')

        bookInfo = [author, title, form, publisher, cost, stock, genre]
        bookData.append(bookInfo)

        print('Title added.')
    print(amount, 'title(s) added.\n')

    # Calculates the average cost of all stocked titles AFTER any additions
    totalIndividualCosts = 0
    for detail in bookData:
        if float(detail[5]) > 0:
            totalIndividualCosts += (float(detail[4]))
    averageTitleCost_after = totalIndividualCosts / len(bookData)

    # Calculates the difference between the two averages 
    # Previously had validation to check which value was the smallest and took that from the largest, however, I don't believe it would make a difference this section only allows for the addition, not reduction, of titles
    averageDifference = averageTitleCost_after - averageTitleCost_before

    # Display the change in number of titles and the average price per title since the new title(s) were added
    print('The current titles in stock is now ', len(bookData), '.' + \
          '\nPreviously ', len(bookData) - amount, ' titles were in stock.', sep='')
    print('\nThe average price of a title is now £', round(averageTitleCost_after, 2), '.' + \
          '\nPreviously £', round(averageTitleCost_before, 2), ' was the average.' + \
          '\nThe difference is £', round(averageDifference, 2), '.', sep='')

    sectionEnd()

def checkAvailability():
    # Print a list of all current titles
    # Ask the user which title they wish to affect
    # Print the selected title's information
    # Provide option to increase/decrease stock level
    # Add/Remove input from the current stock level and display change
    headerText()

    # Display a list of all titles in stock (Allows the user to search easier)
    print('The current titles that could be in stock are as follows:')
    titles = []
    for detail in bookData:
        print(' ', detail[1])
        titles.append(detail[1])
        
    # Get the title the user would like to change the stock level of
    search = input('What title do you wish to search for? Please choose from the above (Case Sensitive): ')

    # Search all lines for the inputed title and return to menu if nothing can be found
    if search in titles:
        for detail in bookData:
            if detail[1] == search:
                print('  Author:', detail[0])
                print('  Genre:', detail[6])
                print('  Publisher:', detail[3])
                if detail[2] == 'pb':
                    print('  Format: Paper Back')
                elif detail[2] == 'hb':
                    print('  Format: Hard Back')
                else:
                    print('  Format: ', detail[2])
                print('  Cost: £', detail[4], sep='')
                if int(detail[5]) > 0:
                    print('  Stock:', detail[5], '\n')
                else: 
                    print('  Stock: Out of Stock\n')

                option = int(input('Please select what you would like to do:' + \
                    '\n (1) Increase Stock Level' + \
                    '\n (2) Decrease Stock Level' + \
                    '\nSelection: '))
                
                # Increase/Decrease the stock level of the selected title by the inputed amount
                if option == 1:
                    increaseAmount = int(input('How much would you like to add to the current stock: '))
                    detail[5] = int(detail[5]) + increaseAmount
                    print( ' Updated Stock:', detail[5])
                elif option == 2:
                    decreaseAmount = int(input('How much would you like to remove from the current stock: '))
                    detail[5] = int(detail[5]) - decreaseAmount
                    if int(detail[5]) > 0:
                        print('  Updated Stock: ', detail[5], '\n')
                    else: 
                        print('  Updated Stock: Out of Stock')
                else:
                    errorHandler()
                # Convert stock levels from into back to a str in order to avoid affect other sections
                detail[5] = str(detail[5])
    else:
        errorHandler()

    sectionEnd()

def orderedDisplay():
    # Get the type of order the user would like to use to display the ventory
    # Create an ordered list that is populated with all bookData, starting with the detail being ordered by
    # Order the titles depending on the user's selection
    # Display an formated list of the stored titles and their respective details
    headerText()

    # Set the order type depending on the selection made by the user
    order = int(input('Please select how you would like to order the output:' + \
                      '\n (1) Title Order  ' + \
                      '\n (2) Genre Order '+ \
                      '\nOrder: '))
    
    print('\nCurrently stocked titles by the selected order:')
    # Put the relevent information first and join the rest of the title's information, then order alphabetically
    orderedList = []
    if order == 1:
        for detail in bookData:
            orderedList.append(', '.join([detail[1]] + detail[:1] + detail[2:]))
    elif order == 2:
        for detail in bookData:
            orderedList.append(', '.join([detail[6]] + detail[:6]))
    else:
        errorHandler()
    orderedList.sort()

    # Separate the book details into separate strings when a ', ' is detected
    for orderedDetail in range(0, len(orderedList)):
        orderedList[orderedDetail] = orderedList[orderedDetail].split(', ')

    # Print a formatted list of the sorted data
    for orderedDetail in orderedList:
        if order == 1:
            print('\n ', orderedDetail[0], ':', sep='')
            print('  Author:', orderedDetail[1])
            print('  Genre:', orderedDetail[6])
            print('  Publisher:', orderedDetail[3])
            if orderedDetail[2] == 'pb':
                print('  Format: Paper Back')
            elif orderedDetail[2] == 'hb':
                print('  Format: Hard Back')
            else:
                print('  Format: ', orderedDetail[2])
            print('  Cost: £', orderedDetail[4], sep='')
            if int(orderedDetail[5]) > 0:
                print('  Stock:', orderedDetail[5])
            else: 
                print('  Stock: Out of Stock')
        elif order == 2:
            print('\n ', orderedDetail[2], ':', sep='')
            print('  Author:', orderedDetail[1])
            print('  Genre:', orderedDetail[0])
            print('  Publisher:', orderedDetail[4])
            if orderedDetail[3] == 'pb':
                print('  Format: Paper Back')
            elif orderedDetail[3] == 'hb':
                print('  Format: Hard Back')
            else:
                print('  Format: ', orderedDetail[3])
            print('  Cost: £', orderedDetail[5], sep='')
            if int(orderedDetail[6]) > 0:
                print('  Stock:', orderedDetail[6])
            else: 
                print('  Stock: Out of Stock')
        else:
            errorHandler()

    sectionEnd()

def chartByGenre():
    # Collect a list of all genres currently in the inventory
    # Display a simple ASCII Bar Chart showing the number of titles in each genre
    headerText()

    # Collect a list of the current genres from bookData
    genres = []
    for detail in bookData:
        genres.append(detail[6])

    # Print a list of each genre and populate the chart depending on number of times each genres appears
    for genre in set(genres):
        genreCount = 0
        for detail in bookData:
            if detail[6] == genre:
                genreCount += 1
        print(genre + ':', '|' * genreCount)

    sectionEnd()

# Utility Functions
def headerText(): # Displays the titleText (Global Variable) and prints an overline equal to the size of the titelText
    print('-' * len(titleText)  + \
          '\n', titleText, '\n', sep='')

def sectionEnd(): # Returns the user to the menu if the selection key is pressed, otherwise ends the progrm
    selection = int(input('\nPlease press (1) to return to the menu. '))
    if selection == 1:
        main()
    else:
        errorHandler()

def errorHandler(): # Returns the user to the menu in the event of an unexpected input
    print('\nInput not recognised!\nReturning to menu...')
    main()

# Initialise Program
main()