from cell import Cell

from pygame.draw import line as pygame_draw_line
from pygame.display import get_surface as pygame_display_get_surface
from pygame.mouse import get_pos as pygame_mouse_get_pos
from pygame.mouse import get_pressed as pygame_mouse_get_pressed
from pygame import Rect as pygame_Rect
from pygame.font import SysFont as pygame_font_SysFont
from pygame.time import get_ticks as pygame_time_get_ticks

from random import choice as random_choice

class Board:

    def __init__(self, board_dimensions, ):

        self.surface = pygame_display_get_surface()
        self.dimensions = board_dimensions

        self.cell_dimensions = (self.dimensions[0] // 3, self.dimensions[1] // 3)
        self.cells = self.create_cells()
        
        self.current_turn = random_choice(("O", "X")) # Player can be "O" or "X" 
        self.cells_remaining = 9 # Used in the event of a tie

        self.text_font = pygame_font_SysFont("Bahnschrift", 75)
        self.reset_timer = 0
        
        # print([(cell.rect.x, cell.rect.y) for cell in self.cells])

    def create_cells(self):

        # Returns a list of all the cells created for the game
        return [Cell(
                        x = (j * self.cell_dimensions[0]),
                        y = (i * self.cell_dimensions[1]),
                        measurements = self.cell_dimensions
                        )
                        for j in range(3) for i in range(3)]

    def handle_cell_collisions(self):

        mouse_pos = pygame_mouse_get_pos()
        mouse_rect = pygame_Rect(mouse_pos[0], mouse_pos[1], 1, 1)

        # Left mouse click
        if pygame_mouse_get_pressed()[0]:
            
            if self.released_button == True:
        
                self.released_button = False
                cell_collided = mouse_rect.collidelist(self.cells)

                # An unchosen cell
                if cell_collided != -1 and self.cells[cell_collided].nature == None:

                    # Set this cell to either "X" or "O"
                    self.cells[cell_collided].nature = self.current_turn

                    # Remove one cell 
                    self.cells_remaining -= 1

                    # Check if anyone won
                    won = self.check_winner()
                    if won:
                        self.current_turn += "#" # Add a temp character to show that the "X" or "O" has won
                        self.reset_timer = pygame_time_get_ticks() # Start the reset timer
                    
                    # Tie
                    elif won == False and self.cells_remaining == 0:
                        self.current_turn = None
                        self.reset_timer = pygame_time_get_ticks() # Start the reset timer

                    else:
                        # Switch turn
                        self.current_turn = "X" if self.current_turn == "O" else "O"


        # Released left mouse click
        else:
            self.released_button = True
    
    def draw_grid(self):
        
        # Vertical
        for i in range(1,3):
            pygame_draw_line(
                            surface = self.surface,
                            color = "BLACK",
                            start_pos = (i * self.cell_dimensions[0], 0),
                            end_pos = (i * self.cell_dimensions[0], self.dimensions[1]),
                            width = 5
                            )
        # Horizontal
        for i in range(1, 3):
            pygame_draw_line(
                            surface = self.surface,
                            color = "BLACK",
                            start_pos = (0, i * self.cell_dimensions[1]),
                            end_pos = (self.dimensions[0], i * self.cell_dimensions[1]),
                            width = 5
                            )
    
    def draw_cells(self):

        for cell in self.cells:
            cell.draw()
    
    def draw_text(self, text, text_colour, font, x, y):
        
        # Render the text as an image without anti-aliasing
        text_image = font.render(text, False, text_colour)
        # Blit the image onto the surface
        self.surface.blit(text_image, (x, y))

    def check_winner(self):
        
        # Horizontal (Rows)
        for i in range(3):
            if self.cells[i].nature != None and self.cells[i].nature == self.cells[i + 3].nature == self.cells[i + 6].nature:
                return True
        
        # Vertical (Columns)
        for i in range(0, 7, 3):
            if self.cells[i].nature != None and self.cells[i].nature == self.cells[i + 1].nature == self.cells[i + 2].nature:
                return True
                
        # Diagonals
        if self.cells[4].nature != None and (
            (self.cells[0].nature == self.cells[4].nature == self.cells[8].nature) or (self.cells[6].nature == self.cells[4].nature == self.cells[2].nature)):
            return True
        
        return False

    def reset_board(self):
        
        self.current_turn = random_choice(("O", "X")) 
        self.cells_remaining = 9 
        self.reset_timer = 0

        # Reset all cells' nature
        for cell in self.cells:
            cell.nature = None

    def run(self):
        
        
        self.draw_grid()
        self.draw_cells()

        # Neither side has won
        if self.current_turn == "X" or self.current_turn == "O":
            self.handle_cell_collisions()

        # Stalemate / Tie or a side has won
        else:

            # 1.5 seconds display time
            if pygame_time_get_ticks() - self.reset_timer <= 1500:

                winner_text = "Tie!" if self.current_turn == None else f"{self.current_turn[:-1]} has won!" 
                text_size = self.text_font.size(winner_text)
                self.draw_text(
                                text = winner_text,
                                text_colour = "GREEN",
                                font = self.text_font,
                                x = (self.surface.get_width() // 2) - (text_size[0] // 2),
                                y = (self.surface.get_height() // 2) - (text_size[1] // 2)
                                )
                
            else:
                self.reset_board()
