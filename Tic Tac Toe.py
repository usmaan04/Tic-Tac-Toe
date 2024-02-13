import pygame,sys
import random
from button import Button
from ai import AI

pygame.init()

# Set up the game window
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
logo = pygame.image.load("assets/logo.png")
pygame.display.set_icon(logo)

# Initialize the game board and current player
board = [[' ' for _ in range(3)] for _ in range(3)]
current_player = 'X'

# Reset the game board and set the current player to 'X'
def reset_board():
    global current_player
    current_player = 'X'
    return [[' ' for _ in range(3)] for _ in range(3)]

# Handle a player's move
def handle_click(row, col):
    global current_player

    if board[row][col] == ' ':
        board[row][col] = current_player

        # Switch player for the next turn
        current_player = 'O' if current_player == 'X' else 'X'

# Draw X and O symbols on the screen
def draw_symbols():
    for row in range(3):
        for col in range(3):
            cell_center_x = int((col + 0.5) * screen_width / 3)
            cell_center_y = int((row + 0.5) * screen_height / 3)

            if board[row][col] == 'X':
                pygame.draw.line(screen, (255, 0, 0), (cell_center_x - 30, cell_center_y - 30), (cell_center_x + 30, cell_center_y + 30), 5)
                pygame.draw.line(screen, (255, 0, 0), (cell_center_x + 30, cell_center_y - 30), (cell_center_x - 30, cell_center_y + 30), 5)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, (0, 0, 255), (cell_center_x, cell_center_y), 30, 5)

# Return a font with a specified size
def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

# Multi line paragraphing
def drawText(surface, text, colour, rect, font, aa=False, bkg=None):
    rect = pygame.Rect(rect)
    y = rect.top
    lineSpacing = -2

    #gets the height of the font
    fontHeight = font.size("Tg")[1]

    while text:
        i = 1

        # determine if the row of text will be outside the created surface box
        if y + fontHeight > rect.bottom:
            break

        # determines the maximum width of line
        while font.size(text[:i])[0] < rect.width and i < len(text):
            i += 1

        # if the text has just been wrapped, then adjust the wrap to the last word      
        if i < len(text): 
            i = text.rfind(" ", 0, i) + 1

        # render the line and displays it to the surface
        if bkg:
            image = font.render(text[:i], 1, colour, bkg)
            image.set_colourkey(bkg)
        else:
            image = font.render(text[:i], aa, colour)

        surface.blit(image, (rect.left, y))
        y += fontHeight + lineSpacing

        # remove the text just blit
        text = text[i:]

    return text

# Draw the game board grid
def draw_board():
    for i in range(1, 3):
        pygame.draw.line(screen, (0, 0, 0), (i * screen_width / 3, 0), (i * screen_width / 3, screen_height), 5)
        pygame.draw.line(screen, (0, 0, 0), (0, i * screen_height / 3), (screen_width, i * screen_height / 3), 5)


def handle_click(row, col):
    global current_player

    if board[row][col] == ' ':
        board[row][col] = current_player

        # Switch player for the next turn
        current_player = 'O' if current_player == 'X' else 'X'

# Check if there's a winner 
def check_winner():
    # Check rows
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] != ' ':
            return board[row][0]

    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]

    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]

    return None  # No winner yet

def instructions():
    while True:
        # Get the current mouse position
        INSTRUCTIONS_POS = pygame.mouse.get_pos()
        
        # Set the window caption to "Instructions"
        pygame.display.set_caption("Instructions")
        
        screen.fill((255, 255, 153))

        # Create a game description text object, display it on a rectangle on the screen
        game_description = "The goal is to be the first player to get three of your symbols (either X or O) in a row, either horizontally, vertically, or diagonally. Decide which player will be 'X' and which will be 'O'. Take turns placing your symbol on an empty spot on the grid."
        description_rect = pygame.draw.rect(screen, (255, 255, 153), pygame.Rect(5, 0, screen_width, screen_height/2))
        drawText(screen, game_description, "Black", description_rect, get_font(20))

        # Create a back button object and display it on the screen
        back_button = Button(image=pygame.image.load("assets/back button.png"), pos=(75, screen_height - 20),     
                            text_input="Back", font=get_font(15), base_colour="White", hovering_colour="Green")
        back_button.changeColour(INSTRUCTIONS_POS)          
        back_button.update(screen)

       # Listen for events like button clicks and mouse movements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Call function to switch screen if button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:                    
                if back_button.checkForInput(INSTRUCTIONS_POS):    
                    main_menu()
                    
        # Update the display to show any changes
        pygame.display.update()

def one_player():
    global board
    board = reset_board()
    while True:
        # Get the current mouse position
        ONE_PLAYER_POS = pygame.mouse.get_pos()
        
        # Set the window caption to "One Player"
        pygame.display.set_caption("One Player")

        # Display the background colour
        screen.fill((255, 255, 153))

        # Create a back button object and display it on the screen
        back_button = Button(image=pygame.image.load("assets/back button.png"), pos=(screen_width/2, screen_height - 250),     
                            text_input="Back", font=get_font(15), base_colour="White", hovering_colour="Green")

        # Create an AI object 
        ai_player = AI('O', check_winner)


        # Draw the board
        draw_board()  

        if current_player == 'O':  # AI's turn
            ai_move = ai_player.make_move(board)
            if ai_move:
                handle_click(ai_move[0], ai_move[1])                

        # Check for a winner
        winner = check_winner()

        
        # Draw X and O symbols
        draw_symbols() 

        #Display winner depending on winner
        if winner:     
            if winner == 'X':
                pygame.draw.rect(screen, (0,0,0), (screen_width / 2 -150, screen_height/4, 300, 70))
                pygame.draw.rect(screen,(255, 255, 153),(screen_width / 2 -145, screen_height-295,290,60))
                screen.blit(get_font(40).render('Player 1 Wins', True, (0, 0, 0)),(75,100))
                back_button.changeColour(ONE_PLAYER_POS)
                back_button.update(screen)
            else:
                pygame.draw.rect(screen, (0,0,0), (screen_width / 2 -150, screen_height/4, 300, 70))
                pygame.draw.rect(screen,(255, 255, 153),(screen_width / 2 -145, screen_height-295,290,60))
                screen.blit(get_font(40).render('Player 2 Wins', True, (0, 0, 0)),(75,100))
                back_button.changeColour(ONE_PLAYER_POS)
                back_button.update(screen)
                
        # Check for a draw
        if not any(' ' in row for row in board) and not winner:
            winner = 'draw'
            pygame.draw.rect(screen, (0,0,0), (screen_width / 2 -150, screen_height/4, 300, 70))
            pygame.draw.rect(screen,(255, 255, 153),(screen_width / 2 -145, screen_height-295,290,60))
            screen.blit(get_font(40).render('Draw', True, (0, 0, 0)),(screen_width - 250, screen_height/4))
            back_button.changeColour(ONE_PLAYER_POS)
            back_button.update(screen)
                
        # Listen for events like button clicks and mouse movements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Call function to switch screen if button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not winner:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    clicked_row = int(mouseY // (screen_height / 3))
                    clicked_col = int(mouseX // (screen_width / 3))
                    handle_click(clicked_row, clicked_col)
                if winner:
                    if back_button.checkForInput(ONE_PLAYER_POS):
                        main_menu()
                        
        # Update the display to show any changes    
        pygame.display.update()
        
def two_player():
    global board
    board = reset_board()
    while True:
        # Get the current mouse position
        TWO_PLAYER_POS = pygame.mouse.get_pos()
        
        # Set the window caption to "Two Player"
        pygame.display.set_caption("Two Player")

        # Display the background colour
        screen.fill((255, 255, 153))

        # Create a back button object and display it on the screen
        back_button = Button(image=pygame.image.load("assets/back button.png"), pos=(screen_width/2, screen_height - 250),     
                            text_input="Back", font=get_font(15), base_colour="White", hovering_colour="Green")

        # Draw the board
        draw_board()

        # Draw X and O symbols
        draw_symbols()  

        # Check for a winner
        winner = check_winner()
        if winner:     
            if winner == 'X':
                pygame.draw.rect(screen, (0,0,0), (screen_width / 2 -150, screen_height/4, 300, 70))
                pygame.draw.rect(screen,(255, 255, 153),(screen_width/2 - 145, screen_height-295, 290, 60))
                screen.blit(get_font(40).render('Player 1 Wins', True, (0, 0, 0)),(75,100))
                back_button.changeColour(TWO_PLAYER_POS)
                back_button.update(screen)
            else:
                pygame.draw.rect(screen, (0,0,0), (screen_width / 2 -150, screen_height/4, 300, 70))
                pygame.draw.rect(screen,(255, 255, 153),(screen_width / 2 -145, screen_height-295, 290, 60))
                screen.blit(get_font(40).render('Player 2 Wins', True, (0, 0, 0)),(75,100))
                back_button.changeColour(TWO_PLAYER_POS)
                back_button.update(screen)

        # Check for a draw
        if not any(' ' in row for row in board) and not winner:
            winner = 'draw'
            pygame.draw.rect(screen, (0,0,0), (screen_width / 2 -150, screen_height/4, 300, 70))
            pygame.draw.rect(screen,(255, 255, 153),(screen_width / 2 -145, screen_height-295, 290, 60))
            screen.blit(get_font(40).render('Draw', True, (0, 0, 0)),(screen_width - 250, screen_height/4))
            back_button.changeColour(TWO_PLAYER_POS)
            back_button.update(screen)

        # Listen for events like button clicks and mouse movements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Call function to allow draw choice or switch screen if button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not winner:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    clicked_row = int(mouseY // (screen_height / 3))
                    clicked_col = int(mouseX // (screen_width / 3))
                    handle_click(clicked_row, clicked_col)
                if winner:
                    if back_button.checkForInput(TWO_PLAYER_POS):
                        main_menu()
                    
        # Update the display to show any changes 
        pygame.display.update()

def main_menu():
    while True:
        # Get the current mouse position
        MENU_MOUSE_POS = pygame.mouse.get_pos()

        # Set the window caption to "Main Main"
        pygame.display.set_caption("Main Menu")

        
        screen.fill((255, 255, 153))
        screen.blit(logo,(screen_width-325,screen_height-325))

        oneplayer_button = Button(image=pygame.image.load("assets/button.png"), pos=(screen_width/2, screen_height - 170),     
                            text_input="One Player", font=get_font(20), base_colour="White", hovering_colour="Green")
        twoplayer_button = Button(image=pygame.image.load("assets/button.png"), pos=(screen_width/2, screen_height - 110),     
                            text_input="Two Player", font=get_font(20), base_colour="White", hovering_colour="Green")
        instruction_button = Button(image=pygame.image.load("assets/button.png"), pos=(screen_width/2, screen_height - 50),     
                            text_input="Instructions", font=get_font(20), base_colour="White", hovering_colour="Green")
        
        # Update all buttons
        for button in [oneplayer_button, twoplayer_button, instruction_button]:                           
            button.changeColour(MENU_MOUSE_POS)          
            button.update(screen)

        # Listen for events like button clicks and mouse movements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Call function to switch screen if button is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:                    
                if instruction_button.checkForInput(MENU_MOUSE_POS):    
                    instructions()
                elif oneplayer_button.checkForInput(MENU_MOUSE_POS):
                    board = reset_board()  # Draw the board
                    one_player()
                elif twoplayer_button.checkForInput(MENU_MOUSE_POS):
                    board = reset_board() 
                    two_player()

        pygame.display.update()

main_menu()

