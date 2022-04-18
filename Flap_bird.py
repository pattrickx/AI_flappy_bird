import sys, pygame
from pygame.draw import rect


class Bird:
    def __init__(self,screen,section_size=50, position=[5,5]) -> None:
        self.screen = screen
        pass

class flap_bird:
    def __init__(self) -> None:
        self bird = Bird


    def reset(self):
        pass

    def colision(self):
        pass

    def user_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP :
                    self.bird.speed[0]=0
                    self.bird.speed[1]=-1

    def draw_game(self):
        ...









if __name__ == '__main__':
    game = flap_bird()
    while True:
        game.user_action()
        game.draw_game()