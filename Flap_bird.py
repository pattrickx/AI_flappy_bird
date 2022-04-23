import math
import sys, pygame
from numpy import tile
import time
from pygame.draw import rect
import random

class Pipe():
    def __init__(self,screen,screen_size,min_hole_size=100,max_hole_size=200,pixel_step=1) -> None:
        self.screen=screen
        self.screen_size=screen_size
        self.min_hole_size = min_hole_size
        self.max_hole_size = max_hole_size
        self.hole_size=self.min_hole_size
        self.init_position = [self.screen_size[0],0]
        self.position = self.init_position.copy()
        self.pixel_step = pixel_step
        self.hole_center=self.screen_size[0]/2
        self.img_up_pipe = pygame.image.load("assets/pipe-green_up.png").convert_alpha()
        self.img_bottom_pipe = pygame.image.load("assets/pipe-green.png").convert_alpha()
        self.section_size = self.img_up_pipe.get_width()
        self.generate_pipe()


    def update_position(self):
        if self.position[0]>-self.section_size:
            self.position[0] -= self.pixel_step
        else:
            self.position = self.init_position.copy()
            self.generate_pipe()
    def generate_pipe(self):
        self.position = self.init_position.copy()
        self.hole_size = random.randrange(self.min_hole_size, self.max_hole_size)
        print(self.hole_size)
        self.hole_center = random.randrange(230, int(self.screen_size[0]-230))
    def draw_pipe(self):
        self.screen.blit(self.img_up_pipe,(self.position[0],(self.hole_center-self.hole_size/2)-self.img_up_pipe.get_height()))
        self.screen.blit(self.img_bottom_pipe,(self.position[0],self.hole_center+self.hole_size/2))

        # rect(self.screen, (0,255,0), (self.position[0],0,self.section_size,self.hole_center-self.hole_size/2))
        # rect(self.screen, (0,255,0), (self.position[0],self.hole_center+self.hole_size/2,self.section_size,self.screen_size[1]-(self.hole_center+self.hole_size/2)))


class Bird:
    def __init__(self,screen, screen_size, position=[280,280],direction=[0,1],color=(0,0,255)) -> None:
        self.screen = screen
        self.screen_size=screen_size
        self.images = [pygame.image.load("assets/yellowbird-downflap.png").convert_alpha(),
                        pygame.image.load("assets/yellowbird-midflap.png").convert_alpha(),
                        pygame.image.load("assets/yellowbird-upflap.png").convert_alpha()]
        self.section_size_w = self.images[0].get_width()
        self.section_size_h = self.images[0].get_height()
        self.position_base = position
        self.position = self.position_base.copy()
        self.direction= direction
        self.color=color
        self.points = 0
        self.max_up_time = 5
        self.up_time = 0
        self.up = False
        self.up_velocit = -0.4
        self.velocit= 0.1
        self.fall_time=0
        self.gravity_ac=0.01
        self.frame = 0

    def reset(self):
        self.up_time = 0
        self.up = False
        self.velocit= 0.1
        self.fall_time=0
        self.position = self.position_base.copy()
    
    def UP(self):
        self.up =True
        self.up_time = 0
        self.velocit= self.up_velocit
        self.fall_time=0
    def draw_bird(self):
        
        self.frame+=1
        if self.frame>2:
            self.frame=0
        self.screen.blit(self.images[self.frame],(self.position[0],self.position[1]))
        # rect(self.screen, self.color, (self.position[0],self.position[1],self.section_size,self.section_size))
    
    def update_position(self):
    #     if self.up and self.position[1]>0:
    #         self.position[1]-=2
    #         self.up_time +=1
    #         if self.up_time>50:
    #             self.up_time = 0
    #             self.up = False
        if self.position[1]<self.screen_size[1]:
            
            self.fall_time+=1
            self.position[1] = self.position[1] +self.velocit*self.fall_time+(self.gravity_ac*self.fall_time**2)/2
            if self.velocit< 0.03:
                self.velocit = self.gravity_ac*self.fall_time+self.up_velocit
            
        if self.position[1]>=self.screen_size[1]-self.section_size_h:
            self.position[1] = self.screen_size[1]-self.section_size_h
            self.velocit = 0


class flap_bird:
    def __init__(self,width=600,height=600) -> None:
        pygame.init()
        pygame.font.init()
        self.size = self.width, self.height =  width,height
        self.screen = pygame.display.set_mode(self.size)
        self.bird = Bird(self.screen,self.size)
        self.pipe = Pipe(self.screen,self.size)
        self.bg_image = pygame.image.load("assets/background-day.png").convert_alpha()
        self.b_image = pygame.image.load("assets/base.png").convert_alpha()
        self.score = 0
        self.points = 0
        self.distance =0 
        self.blackgrond_color = (0,0,0)
        self.start=False
        self.scroll_base=0
        self.scroll_bg=0
        

    def reset(self):
        self.bird.reset()
        self.pipe.generate_pipe()
        self.score = 0
        self.points = 0
        self.distance = 0 
        self.start=False
        pass

    def colision(self):
        if self.bird.position[1]+self.bird.section_size_h>=self.size[1]:
            print("END Game by hit Ground")
            return True
        elif self.pipe.position[0]<=self.bird.position[0]+self.bird.section_size_w<=self.pipe.position[0]+self.pipe.section_size:
            if self.bird.position[1]<=self.pipe.hole_center-(self.pipe.hole_size/2):
                print("END GAME by hit pipe top")
                return True
            elif self.bird.position[1]+self.bird.section_size_h>=self.pipe.hole_center+(self.pipe.hole_size/2):
                print("END GAME by hit pipe botton")
                return True
        return False
    def get_points(self):
        if self.bird.position[0]> self.pipe.position[0]+self.pipe.section_size:
            self.points+=1
            self.score += self.distance
            self.pipe.generate_pipe()
            return True
        return False

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
            self.pipe.update_position()
            self.colision()
    def draw_background(self):
        self.scroll_base+=1
        self.scroll_bg+=0.2
        if self.scroll_base>self.b_image.get_width():
            self.scroll_base=0
        
        if self.scroll_bg>self.bg_image.get_width():
            self.scroll_bg=0
        tiles = math.ceil(self.width/self.bg_image.get_width())+1
        for i in range(0,tiles):
            self.screen.blit(self.bg_image,((i*self.bg_image.get_width())-self.scroll_bg,0))
            self.screen.blit(self.b_image,((i*self.b_image.get_width())-self.scroll_base,self.bg_image.get_height()))
    def game_draw(self):
        self.screen.fill(self.blackgrond_color)
        self.draw_background()
        self.bird.draw_bird()
        self.pipe.draw_pipe()
        pygame.display.update()
        pygame.display.flip()

    def game_draw_player(self):
        self.draw_background()
        self.bird.draw_bird()
        self.pipe.draw_pipe()
        pygame.display.update()
        pygame.display.flip()

    def ai_action(self,move):
        if not self.start:
            self.start = True
        if move[1]==1:
            self.bird.UP()

    def game_step_ai(self,move):

        # reward=1/abs(self.pipe.hole_center - self.bird.position[1]) if abs(self.pipe.hole_center - self.bird.position[1])  >1 else 1
        reward=-5
        self.ai_action(move)
        if self.start:
            self.bird.update_position()
            self.pipe.update_position()
            if self.colision():
                return -10, True, self.score, self.points
            # self.score+=1/abs(self.pipe.hole_center - self.bird.position[1]) if abs(self.pipe.hole_center - self.bird.position[1]) >1 else 1
            if self.pipe.hole_center-self.pipe.hole_size/2<self.bird.position[1]<self.pipe.hole_center+self.pipe.hole_size/2:
                self.score+=self.distance
                reward=5
            if self.get_points():
                reward = 10
            self.distance +=1

        return reward, False, self.score, self.points
        

    def inputs_AI(self):
        # print([self.pipe.hole_center - self.bird.position[1],(self.pipe.position[0]+self.pipe.section_size)-self.bird.position[0]])

        return[self.pipe.hole_center - self.bird.position[1],(self.pipe.position[0]+self.pipe.section_size)-self.bird.position[0]]



if __name__ == '__main__':
    game = flap_bird()
    while True:
        game.game_step()
        game.game_draw_player()

        time.sleep(0.005)