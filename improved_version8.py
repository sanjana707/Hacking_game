# Hacking Version 8
# This is a graphical password guessing game that displays a list of potential computer passwords. 
# The player is allowed up to 4 attempts to guess the password. 
# Each time the user guesses incorrectly, the user is prompted to make a new guess.
# The game indicates whether the player successfully guessed the password or not.


from uagame import Window
from time import sleep
from random import randint, choice

def main():
    location = [0,0]
    attempts = 4
    window = create_window()
    index_page(window)
    display_header(window, location, attempts)
    password = display_password_list(window, location)
    guess = get_guesses(window, password, location, attempts)
    end_game(window, guess, password)

def create_window():
    # Create a window for the game, open it and return it

    window = Window('Hacking', 700, 550)
    window.set_font_name('couriernew')
    window.set_font_size(18)
    window.set_font_color('green')
    window.set_bg_color('black')
    return window

def index_page(window):
    #This page is just a sreen to welcome the player and display the rules
    #The player then has to press the ENTER key to play the game
    welcome_string = ['WELCOME TO ', '', '"HACKING GAME"', '', '', '!!!CHOOSE THE CORRECT PASSWORD FROM THE LIST!!!', '']
    prompt = 'PRESS ENTER TO PLAY GAME'
    
    #  compute y coordinate
    page_height = (len(welcome_string) + 1)*window.get_font_height()
    y_space = window.get_height() - page_height
    line_y = y_space // 2
    
    location=[0 , line_y]
    for string in welcome_string :
        #  compute x coordinate
        x_space = window.get_width() - window.get_string_width(string)
        location[0] = x_space // 2
        display_line(window, string, location)
        line_y = line_y + window.get_font_height()
        
        
     #Prompt the user to play  
    x_space = window.get_width() - window.get_string_width(prompt)
    location[0] = x_space // 2     
    prompt_user(window, prompt, location) 
    
    #  Clear the window
    window.clear()
    

def display_header(window, location, attempts):
    # Display the game header
    # - window is the Window to display in
    # - location is a list containing the int x and y coords of
    # where the header should be displayed and it should be
    # updated for the next output
    # - attempts is the number of guesses allowed

    header = ['DEBUG MODE', str(attempts) + ' ATTEMPT(S) LEFT', '']
    for header_line in header:
        display_line(window, header_line, location)
        
def embed_password(password, size):
    #This function embeds random special characters to the password 
    #It selects the split size of the characters to add a random numbers of characters before 
    #and after the password
    #It returns a fixed length string with password embedded in between the string
    fill = '!@#$%^*()-+=~[]{}'
    embedding = ''
    password_size = len(password)
    split_index = randint(0, size-password_size)
    for index in range(0, split_index):
        embedding = embedding + choice(fill)
    
    embedding= embedding + password
    for index in range(split_index + password_size, size):
        embedding = embedding + choice(fill) 
    return embedding    

def display_password_list(window, location):
    # Display the game passwords, update the location for the next
    # text and return the correct password
    # - window is the Window to display in
    # - location is a list containing the int x and y coords of
    # where the first password should be displayed and it should
    # be updated for the next output

    password_list = ['PROVIDE', 'SETTING', 'CANTINA', 'CUTTING', 'HUNTERS', 'SURVIVE', 'HEARING', 'HUNTING', 'REALIZE', 'NOTHING', 'OVERLAP', 'FINDING', 'PUTTING', 'ACCOUNT', 'ARRANGE', 
                     'BATTERY', 'BROTHER', 'CHAPTER', 'CENTURY', 'CORRECT', 'FORMULA', 'FASHION', 'FREEDOM', 'HOLIDAY', 'INSTALL', 'JOURNEY', 'IMAGINE', 'MAXIMUM', 'MINIMUM', 'OUTLOOK', 
                     'OFFICER', 'PHOENIX', 'PLASTIC', 'PREDICT', 'RAILWAY', 'RESPECT', 'RESPOND', 'SITTING', 'STUDENT', 'TONIGHT', 'VISIBLE', 'VIRTUAL', 'WINNING', 'WAITING', 'TRAFFIC']
    random_list = []
    count = 0
    
    #Create a random password list
    for password in password_list :
         while count!=13:
            i = randint(0, len(password_list)-1)
            random_element = password_list[i]
            random_list.append(random_element)
            password_list.remove(random_element)
            count = count +1
    #Embed asswords with special characters
    for element in random_list:
        password = embed_password(element, 20)
        display_line(window, password, location)
    # Display blank line
    display_line(window,'',location)
    # choose password
    index = randint(0, len(random_list)-1) 
    return random_list[index]

def get_guesses(window, password, location, attempts_left):
    # Input multiple guesses by the player and provide feedback.
    # Return the player's final guess.
    # - window is the Window to display in
    # - password is the str correct password
    # - location is a list containing the int x and y coords of
    # where the first password prompt should be displayed
    # - attempts_left is the number of guesses left

    prompt = 'ENTER PASSWORD >'
    line_x = 0
    guess = prompt_user(window, prompt, location)
    attempts_left = attempts_left - 1
    hint_location = [ window.get_width()//2, 0]

    while guess != password and attempts_left > 0:
        # get next guess
        window.draw_string(str(attempts_left), line_x, window.get_font_height())
        
        display_hint(window, guess, password, hint_location)
        
        check_warning(window, attempts_left)
            
        guess = prompt_user(window, prompt, location)
        
        attempts_left = attempts_left - 1
    return guess

def display_hint(window, guess, password, location):
    #Returns a hint if the player inputs incorrect password
    #Displayed on the top right corner
    #Contains two lines
    #  ---1st line shows incorrect password
    #  ---2nd line shows no. of matching letters in the previous guess
    pause_time = 0.3
    
    #     display 1st line
    string = guess + " INCORRECT"
    window.draw_string(string, location[0], location[1])
    window.update()
    sleep(pause_time)
    location[1] = location[1] + window.get_font_height()
    
    count=0
    index = 0
    max = len(password)
    for letter in guess:
        if (index < max) and (letter == password[index]) :
            count = count +1  
        index = index + 1    
    
    total = str(len(password))
    hint = str(count)+"/"+total+ " IN MATCHING POSITION"
    window.draw_string(hint, location[0], location[1])
    window.update()
    sleep(pause_time)    
    location[1] = location[1] + window.get_font_height()

def check_warning(window, attempts_left):
    # Check whether a lockout warning should be displayed and if so,
    # display it
    # - window is the Window to display in
    # - attempts_left is the number of guesses left

    warning_string = '*** LOCKOUT WARNING ***'
    if attempts_left == 1:
        # display warning
        warning_x = window.get_width() - window.get_string_width(warning_string)
        warning_y = window.get_height() - window.get_font_height()
        window.draw_string(warning_string, warning_x, warning_y)

def end_game(window, guess, password):
    # End the game by displaying the outcome and prompting for
    # an enter.
    # - window is the Window to display in
    # - guess is the player's guess str
    # - password is the correct password string
    # - pause_time is the number of seconds to pause after displaying
    # each result line

    # clear window
    window.clear()

    # create outcome
    if guess == password:
        # create success
        outcome = [guess, '', 'EXITING DEBUG MODE', '', 'LOGIN SUCCESSFUL - WELCOME BACK', '']
        prompt = 'PRESS ENTER TO CONTINUE'
    else:
        # create failure
        outcome = ['YOUR GUESS - '+guess, '','CORRECT PASSWORD - '+password, '', 'LOGIN FAILURE',  'TERMINAL LOCKED', '']
        prompt = 'PRESS ENTER TO EXIT'

    location = display_outcome(window, outcome)

    # prompt for end
    location[0] = (window.get_width() - window.get_string_width(prompt)) // 2
    prompt_user(window, prompt, location)

    # close window
    window.close()

def display_outcome(window, outcome):
    # Display the outcome of the game: success or failure depending
    # on whether the guess equals the password or not. Return
    # the location of the line below the outcome.
    # - window is the Window to display in
    # - guess is the player's guess str
    # - password is the correct password string
    # - pause_time is the number of seconds to pause after displaying
    # each result line

    # compute y coordinate
    string_height = window.get_font_height()
    outcome_height = (len(outcome) + 1)*string_height
    y_space = window.get_height() - outcome_height
    line_y = y_space // 2

    location = [0, line_y]
    for outcome_line in outcome:
     #    compute x coordinate
        x_space = window.get_width() - window.get_string_width(outcome_line)

        location[0] = x_space // 2
        display_line(window, outcome_line, location)
    return location

def display_line(window, string, location):
    # Display a string in the window and update the location
    # - window is the Window to display in
    # - string is the str to display
    # - location is a list containing the int x and int y coords
    # of where the string should be displayed and it should be
    # updated to one "line" below the top left corner of the
    # displayed string

    pause_time = 0.3
    window.draw_string(string, location[0], location[1])
    window.update()
    sleep(pause_time)
    location[1] = location[1] + window.get_font_height()

def prompt_user(window, prompt, location):
    # Draw a prompt, input a string that the user types and
    # return the string
    # - window is the Window to display in
    # - prompt is the str to display
    # - location is a list containing the int x and int y coords
    # of where the prompt should be displayed and it should be
    # updated to one "line" below the top left corner of the
    # displayed prompt

    input = window.input_string(prompt, location[0], location[1])
    location[1] = location[1] + window.get_font_height()
    return input

main()
