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
        
        self.current_turn = random_choice(("O", "X"))
        self.ai_side = random_choice(("O", "X"))

        self.cells_remaining = 9 # Used in the event of a tie

        self.text_font = pygame_font_SysFont("Bahnschrift", 75)
        self.reset_timer = 0
        
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
                    
                    # AI / Player won
                    if won == "X" or won == "O":
                        self.current_turn += "#" # Add a temp character to show that the "X" or "O" has won
                        self.reset_timer = pygame_time_get_ticks() # Start the reset timer
                    
                    # Tie
                    elif won == "Tie":
                        self.current_turn = None
                        self.reset_timer = pygame_time_get_ticks() # Start the reset timer

                    # No winners
                    elif won == None:
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
                return self.cells[i].nature
        
        # Vertical (Columns)
        for i in range(0, 7, 3):
            if self.cells[i].nature != None and self.cells[i].nature == self.cells[i + 1].nature == self.cells[i + 2].nature:
                return self.cells[i].nature
                
        # Diagonals
        if self.cells[4].nature != None and (
            (self.cells[0].nature == self.cells[4].nature == self.cells[8].nature) or (self.cells[6].nature == self.cells[4].nature == self.cells[2].nature)):
            return self.cells[4].nature
        
        # Returns "Tie" if the entire board is filled (there are no available cells)
        return "Tie" if self.cells_remaining == 0 else None

    def reset_board(self):
        
        # The loser should now have the first turn if someone won, else choose randomly
        if self.current_turn == "O#":
            self.current_turn = "X" 
        elif self.current_turn == "X#":
            self.current_turn = "O"
        else:
            self.current_turn = random_choice(("O", "X"))

        self.cells_remaining = 9 
        self.reset_timer = 0

        # Reset all cells' nature
        for cell in self.cells:
            cell.nature = None
    
    def pick_best_move(self):

        # AI is the maximising side
        if self.ai_side == "X":
            best_score = -float("inf")

            for i in range(len(self.cells)):
                
                if self.cells[i].nature == None: # Available
                    
                    # Apply board changes
                    self.cells[i].nature = "X" # if is_maximising else "O"
                    self.cells_remaining -= 1

                    score = self.minimax(False, alpha = -float("inf"), beta = float("inf"))

                    if score > best_score:
                        best_score = score
                        best_move = i

                    # Remove board changes
                    self.cells[i].nature = None
                    self.cells_remaining += 1

        else:
            best_score = float("inf")
            
            for i in range(len(self.cells)):
            
                if self.cells[i].nature == None: # Available
                    
                    # Apply board changes
                    self.cells[i].nature = "O"
                    self.cells_remaining -= 1

                    score = self.minimax(
                                        is_maximising = True, 
                                        alpha = -float("inf"), # Worst possible option for maximising
                                        beta = float("inf") # Worst possible option for minimising
                                        ) 
                    
                    if score < best_score:
                        best_score = score
                        best_move = i

                    # Remove board changes
                    self.cells[i].nature = None
                    self.cells_remaining += 1
    
        # Apply the best move
        self.cells[best_move].nature = self.ai_side
        self.cells_remaining -= 1

        # Check if there was a tie or if the AI won
        result = self.check_winner()
            
        if result == "O" or result == "X":
            self.current_turn += "#"
            self.reset_timer = pygame_time_get_ticks()

        elif result == "Tie":
            self.current_turn = None
            self.reset_timer = pygame_time_get_ticks()

        # No winners
        else:
            # Switch turn
            self.current_turn = "X" if self.current_turn == "O" else "O"
    
    def minimax(self, is_maximising, alpha, beta):

        # Check for a winner / a stalemate
        result = self.check_winner()

        # AI / Player won or a stalemate
        if result != None:
            
            if result == "Tie":
                return 0
            
            # "X": return 1 "O": return -1
            else:
                return -1 if result == "O" else 1
        
        # "X" = Maximising
        if is_maximising:
            best_score = -float("inf")
            for i in range(9):
                
                if self.cells[i].nature == None: # Available
                    
                    self.cells_remaining -= 1
                    self.cells[i].nature = "X"

                    # Set best score as the maximum between the score of picking this cell or the current best score
                    score = self.minimax(False, alpha, beta)
                    best_score = max(best_score, score)

                    self.cells[i].nature = None
                    self.cells_remaining += 1

                    # If beta <= alpha it means that there is a larger maximising value already found, so there is no point searching anymore as "X" will not go down this path
                    alpha = max(alpha, score)
                    if beta <= alpha:
                        break
        
        # "O" = Minimising
        else:
            best_score = float("inf")
            for i in range(9):
                
                if self.cells[i].nature == None: # Available
                    
                    self.cells_remaining -= 1
                    self.cells[i].nature = "O"

                    # Set best score as the minimum between the score of picking this cell or the current best score
                    score = self.minimax(True, alpha, beta)
                    best_score = min(best_score, score)

                    self.cells[i].nature = None
                    self.cells_remaining += 1

                    # If beta <= alpha it means that there is a smaller value already found, so there is no point searching anymore as "O" will not go down this path
                    beta = min(beta, score)
                    if beta <= alpha:
                        break
        
        return best_score

    def run(self):
        
        self.draw_grid()
        self.draw_cells()

        # Still playing and the player's turn
        if (self.current_turn == "X" or self.current_turn == "O"):
            
            # Player's turn
            if self.current_turn != self.ai_side:
                self.handle_cell_collisions()

            # AI's turn
            else:
                self.pick_best_move()

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
