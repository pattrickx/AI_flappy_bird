import sys, pygame
import time
from pygame.draw import rect


class Bird:
    def __init__(self,screen, screen_size,section_size=20, position=[240,300],direction=[0,1],color=(0,0,255)) -> None:
        self.screen = screen
        self.screen_size=screen_size
        self.section_size = section_size
        self.position = position
        self.direction= direction
        self.color=color
        self.points = 0
        self.max_up_time = 5
        self.up_time = 0
        self.up = False
    
    def UP(self):
        self.up =True
        self.up_time = 0
    def draw_bird(self):
        rect(self.screen, self.color, (self.position[0],self.position[1],self.section_size,self.section_size))
    
    def update_position(self):
        if self.up and self.position[1]>0:
            self.position[1]-=2
            self.up_time +=1
            if self.up_time>50:
                self.up_time = 0
                self.up = False
        elif self.position[1]+self.section_size<self.screen_size[1]:
            self.position[1]+=1
        


class flap_bird:
    def __init__(self,width=500,height=700) -> None:
        pygame.init()
        pygame.font.init()
        self.size = self.width, self.height =  width,height
        self.screen = pygame.display.set_mode(self.size)
        self.bird = Bird(self.screen,self.size)
        self.score = 0
        self.blackgrond_color = (0,0,0)
        self.start=False


    def reset(self):
        pass

    def colision(self):
        pass

    def user_action(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP :
                    self.bird.UP()
                    if not self.start:
                        self.start = True

    def game_step(self):
        self.user_action()
        if self.start:
            self.bird.update_position()

    def draw_game(self):
        self.screen.fill(self.blackgrond_color)
        self.bird.draw_bird()
        pygame.display.update()
        pygame.display.flip()
        


if __name__ == '__main__':
    game = flap_bird()
    while True:
        game.game_step()
        game.draw_game()

        time.sleep(0.002)