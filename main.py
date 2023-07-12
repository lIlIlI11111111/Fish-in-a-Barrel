import random
import sys
import os
import datetime
import PyQt5.QtWidgets as QTW
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import pygame
import math
import configparser

maxTitleLen = 1024
randomPrecision = 1000
SAVE_AND_EXIT_CODE = 100

config = configparser.ConfigParser()

class Person:
    def __init__(self):
        self.name = ""
        self.tickets = 0
        self.onCooldown = 0
        self.isIn = 0
    def __init__(self, name, tickets, onCooldown, isIn):
        self.name = name
        self.tickets = tickets
        self.onCooldown = onCooldown
        self.isIn = isIn

def parsePerson(f):
    buffer = f.readline(maxTitleLen)
    newMan = Person()
    token = buffer.split(",")
    #Setting name
    newMan.name = token[0]
    #Setting tickets
    newMan.tickets = int(token[1])
    #Setting onCooldown
    newMan.onCooldown = int(token[2])
    return newMan
    
    

def load_stylesheet(file_path):
    # Check if the file exists
    if not os.path.isfile(file_path):
        # If the file doesn't exist, create a default CSS file with some properties
        with open(file_path, 'w') as file:
            file.write("""
/* Default CSS */
QWidget {
    background-color: #333333;
    color: white;
}
QTableWidget QHeaderView::section {
    background-color: #222222;
    color: #DDDDDD;
}
/* Add more CSS rules here */
""")

    # Load the CSS file
    with open(file_path, 'r') as file:
        stylesheet = file.read()

    return stylesheet

def getData(file):
    if not os.path.isfile(file):
        with open(file, 'w'):
            pass  # Create an empty file

    with open(file, 'r') as f:
        personList = []
        for line in f:
            data = line.strip().split(",")
            name = data[0].strip()
            ticketCount = int(data[1].strip())
            onCooldown = int(data[2].strip())
            isIn = 0

            person = Person(name, ticketCount, onCooldown, isIn)
            personList.append(person)

        return personList

#Increments all attendees who are not currently on cooldown
def incrementAttendees(personList):
    for person in personList:
        if person.isIn and not person.onCooldown:
            person.tickets += 1
    #print("Attendees not on cooldown have been incremented")


def getUserInput(person_list):
    """
    Deprecated, do not use.
    """
    UIfile = open("nameInput.txt", "r") 
    if UIfile is None:
        print("No suitable input file, exiting with error code 1")
        exit(1)
    print("Opened the input file successfully")
    for line in UIfile:
        token = line.split("\n")[0]
        found_match = False
        for p in person_list:
            if p.name == token:
                found_match = True
                if p.onCooldown:
                    break
                p.isIn = 1
        if not found_match:
            print("No match found, adding new user of name: \n", token)
            newMan = Person(token, 0, 0, 1)
            personList.append(newMan)
            print("Set new member as final element in the array")
            print("Their name in the array is: \n", personList[len(personList) - 1].name)
    UIfile.close()
    return

def roll(personList):
    """
    Deprecated, do not use. Replaced by handleSpinner()
    """
    totalTickets = 0
    for person in personList:
        if person.isIn and not person.onCooldown:
            totalTickets += person.tickets
    
    if totalTickets == 0:
        print("Error, no contestants had any tickets. Error with dividing by 0.")
        return -1
    
    r = random.randint(1, totalTickets)
    cumulativeSum = 0
    for i, person in enumerate(personList):
        if person.isIn and not person.onCooldown:
            cumulativeSum += person.tickets
            if cumulativeSum >= r:
                print("With {} tickets, the winner is {}".format(person.tickets, person.name))
                return i
    
    print("A strange error occurred in which no one won. Roll again, maybe, idk?")
    return -1

def rollWrapper(personList):
    hasWinner = False
    while not hasWinner:
        winNum = roll(personList)
        print("Did {} claim their win? (0 for no, 1 for yes, 2 for cancel)".format(personList[winNum].name))
        hasWinner = int(input())
        
        if hasWinner == 1:
            personList[winNum].isIn = 0
            personList[winNum].onCooldown = 1
            personList[winNum].tickets = 0

def writeFile(personList):
    print("Saving data...")
    with open("userDataList.txt", "w") as outFile:
        for i, person in enumerate(personList):
            outFile.write("{},{},{}".format(person.name, person.tickets, person.onCooldown))
            if i < len(personList) - 1:
                outFile.write("\n")

def sortList(personList):
    looping = True
    while looping:
        looping = False
        for i in range(len(personList) - 1):
            if personList[i].tickets < personList[i + 1].tickets:
                looping = True
                personList[i], personList[i + 1] = personList[i + 1], personList[i]
    print("List sorted")

def shouldResetRegularly():
    resetStyle = 0;
    try:
        config.read('config.ini')
        resetStyle = config.get('resetStyle', 'value')
    except (configparser.NoSectionError, configparser.NoOptionError):
        resetStyle = "monthlydebug"
    print("resetStyle read as", resetStyle)
    if resetStyle == "monthly":
        current_date = datetime.datetime.now()
        current_month = current_date.month
        if current_date.day <= 7 and current_month % 2 == 0:
            return "all"
        else:
            return "none"
    else: #other option would be "per user", but this requires a change at every timestep.
        return "decrement"

def tryResetRound(personList):
    shouldResetByDefault =  shouldResetRegularly()
    print("shouldResetRegularly returned", shouldResetByDefault)
    if shouldResetByDefault == "all":
        resetRound(personList)
        print("Round reset successful.")
    elif shouldResetByDefault == "decrement":
        resetViaDecrement(personList)
        print("Decrement-style reset completed")
    elif all(person.isIn == 1 and person.tickets == 0 for person in personList):
        resetRound(personList)
        print("Emergency reset round executed to avoid ")
    else:
        print("Round reset not required.")

def toggleResetStyle():
    config = configparser.ConfigParser()

    # Check if the config file exists
    if not config.read('config.ini'):
        # Create a new config file with the 'resetStyle' section
        config['resetStyle'] = {'value': 'decrement'}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print("New config file created.")
    
    # Check if the 'resetStyle' section exists in the config file
    if 'resetStyle' not in config:
        # Add the 'resetStyle' section with 'decrement' value
        config['resetStyle'] = {'value': 'decrement'}
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print("'resetStyle' section added with 'decrement' value.")
    else:
        # Toggle the value between 'decrement' and 'monthly'
        current_value = config.get('resetStyle', 'value')
        new_value = 'monthly' if current_value == 'decrement' else 'decrement'
        config.set('resetStyle', 'value', new_value)
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print(f"'resetStyle' value toggled to '{new_value}'.")

def resetRound(personList):
    for person in personList:
        person.onCooldown = 0

def resetViaDecrement(personList):
    frequency = -1
    try:
        config.read('config.ini')
        frequency = config.getint('resetStyle', 'resetFrequency')
        print("Read frequency from file as ", frequency)
    except (configparser.NoSectionError, configparser.NoOptionError):
        frequency = 1
        print("No frequency detected, using frequency=1")
    for person in personList:
        if person.onCooldown >= frequency:
            person.onCooldown = 0
        elif person.onCooldown > 0:
            person.onCooldown += 1

def listAll(personList):
    print("Name: tickets, onCooldown, isIn")
    for p in personList:
        print(f"{p.name}: {p.tickets}, {p.onCooldown}, {p.isIn}")       

previous_highest_component = None
current_highest_component = None        

def generate_bright_color():
    global previous_highest_component
    global current_highest_component

    low_value = random.randint(0x00, 0x40)
    random_value = random.randint(0x00, 0xff)

    if current_highest_component is None:
        # Choose a random component as the highest
        current_highest_component = random.choice(["r", "g", "b"])
    elif previous_highest_component is None:
        # Set previous_highest_component if it is None (first call after initialization)
        previous_highest_component = current_highest_component

    # Assign the high value to the chosen component
    if current_highest_component == "r":
        r = random.randint(0xd0, 0xff)
        g, b = low_value, random_value
    elif current_highest_component == "g":
        g = random.randint(0xd0, 0xff)
        r, b = low_value, random_value
    else:  # current_highest_component == "b"
        b = random.randint(0xd0, 0xff)
        r, g = low_value, random_value

    # Update previous_highest_component and current_highest_component
    previous_highest_component = current_highest_component
    current_highest_component = random.choice(["r", "g", "b"])

    return (r, g, b)

def handleSpinner(personList):
    
    #Handling the personList data
    totalTickets = sum(person.tickets for person in personList if person.isIn and not person.onCooldown)
    
    if totalTickets == 0:
        print("Error, no contestants had any tickets. Error with dividing by 0.")
        return -1
    
    sections = []
    for person in personList:
        if person.isIn and not person.onCooldown:
            # Generate a random color for the section
            color = generate_bright_color()

            # Calculate the fraction of tickets for the person
            fraction = person.tickets / totalTickets

            # Create a section dictionary with color, label, and fraction
            section = {"color": color, "label": person.name, "fraction": fraction}

            # Add the section to the sections list
            sections.append(section)
            
    
    
    pygame.init()
    
    window_size = (400, 400)
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Spinner Wheel")
    
    # Define the section colors and labels
    #sections = [
    #    {"color": (255, 0, 0), "label": "Section 1", "fraction": 0.2},
    #    {"color": (0, 255, 0), "label": "Section 2", "fraction": 0.3},
    #    {"color": (0, 0, 255), "label": "Section 3", "fraction": 0.5},
    #]

    running = True
    angle = 0
    spinIsHappening = False
    spinSpeed = 0.1
    spinIsDone = False
    winner = None
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Clear the screen
        screen.fill((0, 0, 0))

        # Calculate the angle range for each section
        start_angle = angle
        for section in sections:
            section["start_angle"] = start_angle
            section["end_angle"] = start_angle + section["fraction"] * 360
            start_angle = section["end_angle"]

        # Draw the sections
        for section in sections:
            # Calculate the section angles in radians
            start_angle_rad = math.radians(section["start_angle"])
            end_angle_rad = math.radians(section["end_angle"])

            # Draw the section arc
            wheel_radius = window_size[0] / 2.5
            wheel_rect = pygame.Rect((window_size[0]/10,window_size[0]/10),(wheel_radius*2,wheel_radius*2))
            pygame.draw.arc(screen, section["color"], wheel_rect, start_angle_rad, end_angle_rad)

            # Calculate the label position
            label_angle = -(section["start_angle"] + section["end_angle"]) / 2
            label_x = int(200 + wheel_radius * pygame.math.Vector2(1, 0).rotate(label_angle).x)
            label_y = int(200 + wheel_radius * pygame.math.Vector2(1, 0).rotate(label_angle).y)

            # Draw the label text
            font = pygame.font.SysFont(None, 20)
            label_text = font.render(section["label"], True, (255, 255, 255))
            label_rect = label_text.get_rect(center=(label_x, label_y))
            screen.blit(label_text, label_rect)

        # Update the spinner angle
        angle -= spinSpeed
        
        if spinIsHappening and not (spinSpeed <= 0):
            spinSpeed = spinSpeed - 0.0005
        
        if spinSpeed < 0.01:
            spinSpeed = 0
            spinIsDone = True
        
        if not spinIsHappening and pygame.mouse.get_pressed(3)[0] == True:
            spinIsHappening = True
            spinSpeed = random.uniform(0.8,1.2)
            
        if spinIsDone:
            target_angle = 90

            for section in sections:
                start_angle = section["start_angle"]
                end_angle = section["end_angle"]

                # Normalize the angles to be between 0 and 360
                start_angle %= 360
                end_angle %= 360

                if start_angle < end_angle:
                    # Case where the section does not span across 0 degrees
                    if start_angle <= target_angle < end_angle:
                        winner = section["label"]
                        break
                else:
                    # Case where the section spans across 0 degrees
                    if start_angle <= target_angle or target_angle < end_angle:
                        winner = section["label"]
                        break
            break

        #draw ticker
        ticker_rect = pygame.Rect((window_size[0]/2)-4, (window_size[0]/10)-10, 8, (window_size[1]/10))
        pygame.draw.rect(screen, 0xffffff, ticker_rect)
        
        # Update the display
        pygame.display.update()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Render the text surface with the winner's name
        text_surface = font.render(winner, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(label_x, label_y))

        # Calculate the position to center the text on the screen
        text_x = (window_size[0] - text_rect.width) // 2
        text_y = (window_size[1] - text_rect.height) // 2

        screen.blit(text_surface, (text_x, text_y))

        pygame.display.flip()
        
        if pygame.mouse.get_pressed(3)[0]:
            break
    # Quit Pygame
    
    pygame.quit()
    return winner


        
        
class PersonListWidget(QTW.QPlainTextEdit):
    """
    Custom widget for displaying a list of persons.

    This widget extends QPlainTextEdit and provides functionality to load and display
    a list of Person objects.

    Args:
        parent (QWidget): Optional parent widget.

    Example:
        personListWidget = PersonListWidget()
        personListWidget.loadPersonList(personList)

    Note:
        - This widget is read-only and cannot be edited by the user.

    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)  # Set the widget to be read-only

    def loadPersonList(self, personList):
        """
        Load and display a list of persons in the widget.

        Args:
            personList (list): A list of Person objects.

        Returns:
            None

        Example:
            personListWidget = PersonListWidget()
            personListWidget.loadPersonList(personList)

        This method takes a list of Person objects and generates a formatted string
        representation of each person's name, tickets, and onCooldown attributes. The
        generated text is set as the content of the widget, allowing the list to be
        displayed.

        Note:
            - The personList argument should be a list of Person objects.
        """
        text = ""
        for person in personList:
            text += f"{person.name}, {person.tickets}, {person.onCooldown}\n"

        self.setPlainText(text)

def storePlainTextToFile(text_edit, filename):
    """
    Stores the plain text content of a QPlainTextEdit widget into a file.

    Args:
        text_edit (QPlainTextEdit): The QPlainTextEdit widget containing the text to be stored.
        filename (str): The name of the file to store the text in.

    Returns:
        None

    Raises:
        IOError: If an error occurs while writing the file.

    Example:
        storePlainTextToFile(text_edit, "output.txt")

    This function takes the plain text content of a QPlainTextEdit widget and saves it into
    a file with the specified filename. If the file already exists, its contents will be overwritten.
    If the file does not exist, a new file will be created.

    Note:
        - The text_edit argument should be an instance of QPlainTextEdit.
        - The filename argument should be a string representing the desired filename.
    """
    text = text_edit.toPlainText()
    with open(filename, 'w') as file:
        file.write(text)

def loadPlainTextFromFile(text_edit, filename):
    """
    Loads the contents of a text file into a QPlainTextEdit widget.

    Args:
        text_edit (QPlainTextEdit): The QPlainTextEdit widget to load the text into.
        filename (str): The name of the file to load the text from.

    Returns:
        None

    Raises:
        FileNotFoundError: If the specified file does not exist.

    Example:
        loadPlainTextFromFile(text_edit, "input.txt")

    This function reads the contents of a text file with the specified filename and sets the text
    of the QPlainTextEdit widget to the content of the file. If the file does not exist, a
    FileNotFoundError is raised.

    Note:
        - The text_edit argument should be an instance of QPlainTextEdit.
        - The filename argument should be a string representing the name of the file.
    """
    try:
        with open(filename, 'r') as file:
            text = file.read()
            text_edit.setPlainText(text)
    except FileNotFoundError:
        with open(filename, 'w+') as file:
            # Write some default content if desired
            default_text = ""
            file.write(default_text)
            text_edit.setPlainText(default_text)

def blacklistCull(blacklist, personList):
    """
    Updates the 'isIn' attribute of persons in the personList based on the blacklist.

    Args:
        blacklist (list): A list of person names to be blacklisted.
        personList (list): A list of Person objects.

    Returns:
        None

    Example:
        blacklist = ["Alice", "Bob"]
        personList = [person1, person2, person3]
        blacklistCull(blacklist, personList)

    This function iterates over the personList and checks if the 'name' attribute of each person
    exists in the blacklist. If it does, the 'isIn' attribute of that person is set to 0.

    Note:
        - The blacklist argument should be a list of strings representing person names.
        - The personList argument should be a list of Person objects.
        - The 'isIn' attribute of a Person object is updated in-place.
    """
    for person in personList:
        if person.name in blacklist:
            person.isIn = 0



class DataLossDialog(QTW.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.custom_result = None
        self.setWindowTitle("Data Loss Warning")

        self.initUI()

    def initUI(self):
        # Add a label with the warning message
        label = QTW.QLabel("Warning: Unsaved data will be lost. Do you want to continue?")
        label.setWordWrap(True)

        # Create buttons for different actions
        button_save_exit = QTW.QPushButton("Save and Exit")
        button_exit = QTW.QPushButton("Exit without Saving")
        button_cancel = QTW.QPushButton("Cancel")

        # Connect button signals to respective slots
        button_save_exit.clicked.connect(self.saveAndExit)
        button_exit.clicked.connect(self.exitWithoutSaving)
        button_cancel.clicked.connect(self.cancel)

        # Create a layout to organize the widgets
        layout = QTW.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(button_save_exit)
        layout.addWidget(button_exit)
        layout.addWidget(button_cancel)

        self.setLayout(layout)

    def saveAndExit(self):
        self.custom_result = SAVE_AND_EXIT_CODE
        self.accept()  # Close the dialog and return SAVE_AND_EXIT_CODE

    def exitWithoutSaving(self):
        self.accept()  # Close the dialog and return QDialog.Accepted

    def cancel(self):
        self.reject()  # Close the dialog and return QDialog.Rejected


class MainWindow(QTW.QWidget):
    def __init__(self, personList):
        super().__init__()
        self.resize(2000, 1000)  # Set initial width to 800 and height to 600
        self.personList = personList

        self.initUI()
    def loadPersonListData(self):
        # Clear the table
        self.tableWidget.clear()

        # Set the column count
        column_count = 4
        self.tableWidget.setColumnCount(column_count)

        # Set the header labels
        header_labels = ["Name", "Ticket", "onCooldown", "isIn"]
        self.tableWidget.setHorizontalHeaderLabels(header_labels)

        # Set the row count
        row_count = len(self.personList)
        self.tableWidget.setRowCount(row_count)

        # Populate the table with data
        for row, person in enumerate(self.personList):
            name_item = QTW.QTableWidgetItem(person.name)
            ticket_item = QTW.QTableWidgetItem(str(person.tickets))
            cooldown_item = QTW.QTableWidgetItem(str(person.onCooldown))
            isIn_item = QTW.QTableWidgetItem(str(person.isIn))

            self.tableWidget.setItem(row, 0, name_item)
            self.tableWidget.setItem(row, 1, ticket_item)
            self.tableWidget.setItem(row, 2, cooldown_item)
            self.tableWidget.setItem(row, 3, isIn_item)

        # Resize the columns to fit the contents
        self.tableWidget.resizeColumnsToContents()
    def initUI(self):
        self.setWindowTitle("Fish in a Barrel")
        self.resize(800, 600)  # Set initial width to 800 and height to 600

        # Create a vertical layout
        layout = QTW.QGridLayout()

        # Create a label for the instructions
        #label = QTW.QLabel("Select an option:")
        #layout.addWidget(label)
        
        # Create group boxes
        rollingGroupBox = QTW.QGroupBox("Rolling:")
        rollingLayout = QTW.QGridLayout()
        rollingGroupBox.setLayout(rollingLayout)
        layout.addWidget(rollingGroupBox, 2, 1)
        
        loadingStuffGroupBox = QTW.QGroupBox("Loading:")
        loadingStuffLayout = QTW.QVBoxLayout()
        loadingStuffGroupBox.setLayout(loadingStuffLayout)
        layout.addWidget(loadingStuffGroupBox, 1, 2)
        loadingFromSiteGroupBox = QTW.QGroupBox()
        loadingFromSiteLayout = QTW.QHBoxLayout()
        loadingFromSiteGroupBox.setLayout(loadingFromSiteLayout)
        loadingStuffLayout.addWidget(loadingFromSiteGroupBox)
        
        functionsGroupBox = QTW.QGroupBox("Functions")
        functionsLayout = QTW.QVBoxLayout()
        functionsGroupBox.setLayout(functionsLayout)
        layout.addWidget(functionsGroupBox, 1, 1)
        
        #Functions buttons
        button1 = QTW.QPushButton("Default procedure (CTRL + SHIFT + Enter)")
        button1.clicked.connect(self.handleOption1)
        functionsLayout.addWidget(button1)
        
        #resetStyle things
        resetGroupBox = QTW.QGroupBox("Reset Style:")
        resetLayout = QTW.QVBoxLayout()
        resetGroupBox.setMaximumHeight(100)
        resetGroupBox.setLayout(resetLayout)
        functionsLayout.addWidget(resetGroupBox)
        
        button2 = QTW.QPushButton("Toggle reset style")
        button2.clicked.connect(self.handleOption2)
        resetLayout.addWidget(button2)
        
        config.read('config.ini')
        self.resetSlider = QTW.QSlider(Qt.Horizontal)
        self.resetSlider.setMinimum(1)
        self.resetSlider.setMaximum(10)
        self.resetSlider.setTickPosition(QTW.QSlider.TicksBelow)
        self.resetSlider.setTickInterval(1)
        self.resetSlider.setValue(self.getConfigValue())
        self.resetSlider.valueChanged.connect(self.updateConfig)
        self.resetSlider.setTickPosition(QTW.QSlider.TicksBothSides)
        self.resetSlider.setTickInterval(1)
        self.resetSlider.setSingleStep(1)
        
        #sliderLayout = QTW.QGridLayout()
        #sliderGroupBox = QTW.QGroupBox()
        #sliderGroupBox.setLayout(sliderLayout)
        #sliderLayout.addWidget(self.resetSlider, 0, 0, 1, 3)
        #for i in range(11):
        #    label = QTW.QLabel(str(i))
        #    sliderLayout.addWidget(label, 1, i)
        #resetLayout.addWidget(sliderGroupBox)
        resetLayout.addWidget(self.resetSlider)
        

        #Rest of the functions buttons
        button3 = QTW.QPushButton("Increment active users")
        button3.clicked.connect(self.handleOption3)
        functionsLayout.addWidget(button3)

        button5 = QTW.QPushButton("Save data to data file (CTRL + S)")
        button5.clicked.connect(self.handleOption5)
        functionsLayout.addWidget(button5)

        button7 = QTW.QPushButton("Sort the list")
        button7.clicked.connect(self.handleOption7)
        functionsLayout.addWidget(button7)

        button8 = QTW.QPushButton("Manual Reset Round")
        button8.clicked.connect(self.handleOption8)
        functionsLayout.addWidget(button8)

        button9 = QTW.QPushButton("Exit from the program (CTRL + W) OR (CTRL + Q)")
        button9.clicked.connect(self.handleOption9)
        functionsLayout.addWidget(button9)
        
        self.tableWidget = QTW.QTableWidget()
        layout.addWidget(self.tableWidget, 2, 2)
        self.tableWidget.setEditTriggers(QTW.QAbstractItemView.NoEditTriggers)

        # Create a delegate and set it for the table widget
        delegate = QTW.QStyledItemDelegate()
        self.tableWidget.setItemDelegate(delegate)


        #Loading stuff buttons
        self.streamURLField = QTW.QPlainTextEdit()
        self.streamURLField.setMaximumHeight(50)  # Set the maximum height
        self.streamURLField.setMaximumWidth(300)  # Set the maximum width
        self.streamURLField.setPlaceholderText("Your Stream URL")
        loadingFromSiteLayout.addWidget(self.streamURLField)
        
        self.nameField = QTW.QPlainTextEdit()
        self.nameField.setPlaceholderText("Names go here")
        loadingStuffLayout.addWidget(self.nameField)
        
        loadFromSiteButton = QTW.QPushButton("Load")
        loadFromSiteButton.clicked.connect(self.loadFieldFromStream)
        loadingFromSiteLayout.addWidget(loadFromSiteButton)
        
        loadFromFieldButton = QTW.QPushButton("Load")
        loadFromFieldButton.clicked.connect(self.getInputFromField)
        loadingStuffLayout.addWidget(loadFromFieldButton)
        
        self.blacklistField = QTW.QPlainTextEdit()
        self.blacklistField.setPlaceholderText("Blacklist")
        loadingStuffLayout.addWidget(self.blacklistField)
        
        #Rolling buttons
        self.rollLabel = QTW.QLabel("Click 'Roll' to start rolling.")
        self.rollLabel.setMaximumWidth(1000)
        self.rollLabel.setWordWrap(True)
        self.rollButton = QTW.QPushButton("Roll")
        self.acceptButton = QTW.QPushButton("Accept Winner")
        self.denyButton = QTW.QPushButton("Deny Winner")
        self.cancelButton = QTW.QPushButton("Cancel Rolling")

        #Placing rolling buttons on rolling widget
        rollingLayout.addWidget(self.rollLabel, 1, 1)
        rollingLayout.addWidget(self.rollButton, 2, 1)
        rollingLayout.addWidget(self.acceptButton, 3, 1)
        rollingLayout.addWidget(self.denyButton, 3, 2)
        rollingLayout.addWidget(self.cancelButton, 3, 3)


        self.rollButton.clicked.connect(self.startRolling)
        self.acceptButton.clicked.connect(self.acceptWinner)
        self.denyButton.clicked.connect(self.denyWinner)
        self.cancelButton.clicked.connect(self.cancelRolling)
        
        self.acceptButton.setEnabled(False)
        self.denyButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
        
        self.setLayout(layout)
        
        self.handleOption7()
        self.loadStreamNameFromFile()
        self.loadBlacklistFromFile()
    """def loadPersonListData(self):
        # Load the data from personList into the text box
        header = "Name:\tTicket:\tonCooldown:\tisIn\n"
        data = ""
        for person in self.personList:
            formatted_data = "{}\t{}\t{}\t{}\n".format(
                person.name.ljust(20),
                str(person.tickets).ljust(10),
                str(person.onCooldown).ljust(15),
                str(person.isIn).ljust(5)
            )
            data += formatted_data
        self.textEdit.setPlainText(header + data)"""
    
    def keyPressEvent(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Q:
            # Handle CTRL+Q hotkey
            self.handleOption9()
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_W:
            # Handle CTRL+W hotkey
            self.handleOption9()
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_S:
            # Handle CTRL+S hotkey
            self.handleOption5()
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_L:
            # Handle CTRL+S hotkey
            self.getInputFromField()
        if (event.modifiers() == (Qt.ControlModifier | Qt.ShiftModifier) and
                event.key() == Qt.Key_Return):
            #Handle CTRL+SHIFT+Enter
            self.handleOption1()
    
    def startRolling(self):
        
        winnername = handleSpinner(self.personList)
        winnerSelected = False
        for person in self.personList:
            if winnername == person.name:
                self.rollButton.setEnabled(False)
                self.acceptButton.setEnabled(True)
                self.denyButton.setEnabled(True)
                self.cancelButton.setEnabled(True)
                self.currentWinner = person
                self.rollLabel.setText("With {} tickets, the winner is {}".format(person.tickets, person.name))
                winnerSelected = True
                break
        if(not winnerSelected):
            self.rollLabel.setText("A strange error occurred in which no one won. Roll again, maybe, idk?")
            
    def saveStreamNameToFile(self):
        storePlainTextToFile(self.streamURLField, "streamname.txt")
        return
    
    def loadStreamNameFromFile(self):
        loadPlainTextFromFile(self.streamURLField, "streamname.txt")
        return
        
    def saveBlacklistToFile(self):
        storePlainTextToFile(self.blacklistField, "blacklist.txt")
        return
    
    def loadBlacklistFromFile(self):
        loadPlainTextFromFile(self.blacklistField, "blacklist.txt")
        return
    
    def loadFieldFromStream(self):
        self.saveStreamNameToFile()
        
        #TODO fill self.nameField via a web getter (maybe Panda)
        
        #Blacklist handling
        nameOfStreamer = self.streamURLField.toPlainText().split('/')[-1]
        text = self.blacklistField.toPlainText()
        if nameOfStreamer not in text:
            text+="\n"+nameOfStreamer
            self.blacklistField.setPlainText(text)
        
    
    def getInputFromField(self):
        if self.nameField.toPlainText() == "":
            print("No text in input field")
            return
        print("Viewed field successfully")
        print(self.nameField.toPlainText())
        for line in self.nameField.toPlainText().splitlines():
            token = line.split("\n")[0]
            found_match = False
            for p in self.personList:
                if p.name == token:
                    found_match = True
                    if p.onCooldown:
                        break
                    p.isIn = 1
            if not found_match:
                print("No match found, adding new user of name: \n", token)
                newMan = Person(token, 0, 0, 1)
                self.personList.append(newMan)
                print("Set new member as final element in the array")
                print("Their name in the array is: \n", self.personList[len(self.personList) - 1].name)
        blacklistCull(self.blacklistField.toPlainText().split("\n"), self.personList)
        self.handleOption7()
        return
    
    def getConfigValue(self):
        # Get the 'resetStyle' value from the config file
        return int(config.get('resetStyle', 'resetfrequency', fallback='1'))
    
    def updateConfig(self, value):
        # Update the 'resetStyle' value in the config file
        config.set('resetStyle', 'resetfrequency', str(value))
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print(f"'resetStyle' value updated: {value}")
    
    def dataLossWarning(self):
        self.saveStreamNameToFile()
        self.saveBlacklistToFile()
        if self.verifyData():
            sys.exit()
        
        dialog = DataLossDialog()
        result = dialog.exec_()
        customResult = dialog.custom_result
        #print("Result: ", result)
        #print("customResult: ", customResult)
        
        if customResult == SAVE_AND_EXIT_CODE:
            # User clicked "Save and Exit"
            print("Saving and Exiting")
            self.handleOption5()
            #print("Data SHOULD be saved...")
            sys.exit()
        elif result == QTW.QDialog.Accepted:
            # User clicked "Exit without Saving"
            print("Exit without Saving")
            sys.exit()
        elif result == QTW.QDialog.Rejected:
            # User clicked "Cancel"
            print("Canceling")

        dialog.deleteLater()

        
        
    def verifyData(self):
        file = "userDataList.txt"
        if not os.path.isfile(file):
            return False

        fileData = getData(file)

        if len(self.personList) != len(fileData):
            return False

        for person1, person2 in zip(self.personList, fileData):
            if person1.name != person2.name:
                return False
            if person1.tickets != person2.tickets:
                return False
            if person1.onCooldown != person2.onCooldown:
                return False

        return True



    def acceptWinner(self):
        self.rollLabel.setText(f"Accepted {self.currentWinner.name} as winner. Do something here.")
        self.currentWinner.tickets=0
        self.currentWinner.onCooldown = 1
        self.currentWinner.isIn = 0
        
        self.rollButton.setEnabled(True)
        self.acceptButton.setEnabled(False)
        self.denyButton.setEnabled(False)
        self.cancelButton.setEnabled(False)
        self.handleOption7()

    def denyWinner(self):
        self.rollLabel.setText("Winner denied. Finding new winner...")
        self.startRolling()

    def cancelRolling(self):
        self.rollLabel.setText("Rolling canceled.")
        self.rollButton.setEnabled(True)
        self.acceptButton.setEnabled(False)
        self.denyButton.setEnabled(False)
        self.cancelButton.setEnabled(False)

    # Button click event handlers for each option
    def handleOption1(self):
        #getUserInput(self.personList)
        self.saveStreamNameToFile()
        self.loadFieldFromStream()
        self.getInputFromField()
        tryResetRound(self.personList)
        incrementAttendees(self.personList)
        self.loadPersonListData()
        sortList(self.personList)
        #listAll(self.personList)
        self.startRolling()

    def handleOption2(self):
        toggleResetStyle()

    def handleOption3(self):
        incrementAttendees(self.personList)
        self.loadPersonListData()
        print("Attendees incremented")
        #listAll(self.personList)

    def handleOption4(self):
        rollWrapper(self.personList)

    def handleOption5(self):
        self.saveBlacklistToFile()
        writeFile(self.personList)

    def handleOption7(self):
        sortList(self.personList)
        self.loadPersonListData()
        #listAll(self.personList)

    def handleOption8(self):
        resetRound(self.personList)
        self.loadPersonListData()
        #listAll(self.personList)

    def handleOption9(self):
        #print("Option9 start")
        self.dataLossWarning()
        #print("Option9 end")
        #sys.exit()
        
    def closeEvent(self, event):
        # Perform your custom actions here, e.g., show data loss warning
        self.dataLossWarning()

def main():
    # Open the file
    file_path = "userDataList.txt"
    personList = getData(file_path)
    print("Processed file userDataList.txt and parsed data for", len(personList), "persons")
    chooserNum = -1
    cont = 1
    
    app = QTW.QApplication(sys.argv)
    stylesheet_path = 'styles.css'  # Path to your CSS file
    stylesheet = load_stylesheet(stylesheet_path)
    app.setStyleSheet(stylesheet)
    window = MainWindow(personList)
    window.resize(1500,1000)
    icon = QIcon("./Icon.jpg")
    window.setWindowIcon(icon)
    window.showMaximized()
    sys.exit(app.exec_())

    
    #TODO implement

if __name__ == "__main__":
    main()
