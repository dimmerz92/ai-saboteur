from Game import Game
import constants as C

import pygame
import time

class Controller:
    def __init__(self):
        self.game = Game()

    def turn(self):
        agent = self.game.whos_turn()
        percepts = self.game.get_percepts()
        action = agent.sense_think_act(percepts)
        self.game.state_transition(action)
        return action
    
    def draw_gameboard(self, screen):
        grid = self.game.get_percepts()["gameboard"]

        for row in range(C.ROWS):
            for col in range(C.COLS):
                cell = grid[row][col]
                if cell:
                    img = pygame.image.load(cell.img["path"])
                    if cell.img["angle"] > 0:
                        pygame.transform.rotate(img, cell.img["angle"])
                    card = pygame.transform.scale(img,
                                                  (C.CELL_SIZE, C.CELL_SIZE))
                    screen.blit(card, (col * C.CELL_SIZE, row * C.CELL_SIZE))

    def draw_text(self, screen, text):
        font = pygame.font.SysFont("Helvetica", 20)
        size = font.size(text)
        display = font.render(text, True, (0, 0, 0))
        screen.blit(display, ((C.COLS * C.CELL_SIZE - size[0]) / 2,
                              5 + C.ROWS * C.CELL_SIZE))

    
    def begin(self, screen):
        running = True
        clock = pygame.time.Clock()
        self.draw_gameboard(screen)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            time.sleep(1)
            self.turn()

            screen.fill((255, 255, 255))
            self.draw_gameboard(screen)
            self.draw_text(screen, "HELLO")

            pygame.display.flip()
            clock.tick(C.FPS)

        pygame.quit()

        
        

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(C.WINDOW_SIZE)
    pygame.display.set_caption("Saboteur Game")
    


    
    controller = Controller()
    controller.begin(screen)





    # for _ in range(100):
    #     action = controller.turn()
    #     print(action)