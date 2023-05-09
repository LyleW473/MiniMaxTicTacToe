from pygame import Rect as pygame_Rect
from pygame.display import get_surface as pygame_display_get_surface
from pygame.draw import line as pygame_draw_line
from pygame.draw import circle as pygame_draw_circle

class Cell:

    def __init__(self, x, y, measurements):

        self.surface = pygame_display_get_surface()
        
        self.rect = pygame_Rect(
                                x, 
                                y, 
                                measurements[0], 
                                measurements[1]
                                )

        self.nature = None # Nought or Cross
    
    def draw(self):

        match self.nature:

            case "O":
                pygame_draw_circle(
                                    surface = self.surface, 
                                    color = "BLUE", 
                                    center = ((self.rect.x + (self.rect.width / 2)), (self.rect.y + (self.rect.height / 2))),
                                    radius = self.rect.width / 2,
                                    width = 5
                                )


            case "X":
                pygame_draw_line(
                                surface = self.surface, 
                                color = "RED",
                                start_pos = (self.rect.x, self.rect.y),
                                end_pos = (self.rect.x + self.rect.width, self.rect.y + self.rect.height),
                                width = 5
                                )
                pygame_draw_line(
                                surface = self.surface, 
                                color = "RED",
                                start_pos = (self.rect.x + self.rect.width, self.rect.y),
                                end_pos = (self.rect.x, self.rect.y + self.rect.height),
                                width = 5
                                )
