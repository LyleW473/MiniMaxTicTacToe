from cell import Cell

from pygame.draw import line as pygame_draw_line
from pygame.display import get_surface as pygame_display_get_surface
from pygame.mouse import get_pos as pygame_mouse_get_pos
from pygame.mouse import get_pressed as pygame_mouse_get_pressed
from pygame import Rect as pygame_Rect

from random import choice as random_choice

class Board:

    def __init__(self, board_dimensions, ):

        self.surface = pygame_display_get_surface()
        self.dimensions = board_dimensions

        self.cell_dimensions = (self.dimensions[0] // 3, self.dimensions[1] // 3)
        self.cells = self.create_cells()

        self.current_turn = random_choice(("O", "X")) # Player can be "O" or "X" 
        
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

                    # ADD METHOD TO CHECK WINNER HERE

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
        
    def run(self):

        self.draw_grid()
        self.draw_cells()
        self.handle_cell_collisions()
