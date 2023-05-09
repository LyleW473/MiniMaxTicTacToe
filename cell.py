from pygame import Rect as pygame_Rect

class Cell:

    def __init__(self, x, y, measurements):
        
        self.rect = pygame_Rect(
                                x, 
                                y, 
                                measurements[0], 
                                measurements[1]
                                )
    