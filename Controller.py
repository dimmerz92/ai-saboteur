from Game import Game
from agent_logic import random_behaviour, intelligent_behaviour
import constants as C

import pygame
import time
        
class Controller:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode(C.WINDOW_SIZE)
        self.game = Game(intelligent_behaviour)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Saboteur Game")
        
        self.draw_gameboard()

    def turn(self):
        agent = self.game.whos_turn()
        percepts = self.game.get_percepts()
        card = self.game.draw()
        action = agent.sense_think_act(percepts, card)
        self.game.state_transition(action, self.special_card_callback)
        return action
    
    def draw_gameboard(self, gameboard=None):
        grid = None
        if gameboard is None:
            grid = self.game.get_percepts()["gameboard"]
        else:
            grid = gameboard

        for row in range(C.ROWS):
            for col in range(C.COLS):
                cell = grid[row][col]
                if cell:
                    img = pygame.image.load(cell.img["path"])
                    if cell.img["angle"] > 0:
                        pygame.transform.rotate(img, cell.img["angle"])
                    card = pygame.transform.scale(img,
                                                  (C.CELL_SIZE, C.CELL_SIZE))
                    self.screen.blit(card,
                                     (col * C.CELL_SIZE, row * C.CELL_SIZE))

    def draw_text(self, text):
        font = pygame.font.SysFont("Helvetica", 20)
        size = font.size(text)
        display = font.render(text, True, (0, 0, 0))
        self.screen.blit(display, ((C.COLS * C.CELL_SIZE - size[0]) / 2,
                              5 + C.ROWS * C.CELL_SIZE))
        
    def special_card_callback(self, action):
        (target, card) = action
        img = pygame.image.load(card.img["path"])

        if card.name in ["SABOTAGE", "MEND"]:
            card = pygame.transform.scale(img, (C.CELL_SIZE, C.CELL_SIZE))
            self.screen.blit(img, (500,500))
        else:
            gameboard = self.game.get_percepts()["gameboard"]
            gameboard[target] = card
            self.draw_gameboard(gameboard)

        pygame.display.flip()
        time.sleep(1)

    
    def begin(self):
        running = True
        game_over = False
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            if not game_over:
                time.sleep(1)
                agent = self.game.whos_turn(True)
                self.turn()
                self.screen.fill((255, 255, 255))
                self.draw_gameboard()
                self.draw_text(agent)
                

                pygame.display.flip()
                self.clock.tick(C.FPS)

        pygame.quit()

if __name__ == "__main__":
    controller = Controller()
    controller.begin()