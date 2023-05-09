from pygame import init as pygame_init
from pygame.display import set_caption as pygame_display_set_caption
from pygame.display import update as pygame_display_update
from pygame.display import set_mode as pygame_display_set_mode
from pygame.event import get as pygame_event_get
from pygame import QUIT as pygame_QUIT
from pygame import quit as pygame_quit
from sys import exit as sys_exit
from board import Board 

class Main:
    def __init__(self):

        # Pygame set-up
        pygame_init()

        # Set the caption
        pygame_display_set_caption("MiniMaxTicTacToe")

        # Display
        dimensions = (900, 900)
        self.screen = pygame_display_set_mode(dimensions)

        # Board
        self.board = Board(board_dimensions = dimensions)
    
    def run(self):
 
        while True:
            
            # Fill screen
            self.screen.fill("WHITE")

            # Runs board methods
            self.board.run()
            
            # Event handler
            self.handle_events()
            
            # Update display
            pygame_display_update() 

    def handle_events(self):

        for event in pygame_event_get():
            
            if event.type == pygame_QUIT:
                pygame_quit()
                sys_exit()

if __name__ == "__main__":
    # Instantiate main and run it
    main = Main()
    main.run()