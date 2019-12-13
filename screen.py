import pygame
from bus import Bus
import numpy as np

white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 

class Screen:

    def __init__(self):
        pygame.init()

        self.nes = Bus()
        self.asm = self.nes.load_test()

        self.x = 780
        self.y = 480

        self.surface = pygame.display.set_mode((self.x,self.y))
        self.font = pygame.font.Font('freesansbold.ttf', 15)

        """
        defines ram txt
        """
        

        

        pygame.display.set_caption("pyNES")

    
    def turn_on(self):
        while True:
            self.surface.fill(blue)
            for event in pygame.event.get() :
        
                    

                    self.draw_code()
                    self.draw_ram()
                    self.draw_reg()

                    if event.type == pygame.QUIT : 
                        pygame.quit()  
                        quit() 
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.nes.step_test()
            
                
                    pygame.display.update() 


    def draw_code(self):
        key_index = list(self.asm.keys()).index(self.nes.cpu.pc)
        for i in range(-5,6):
            key = list(self.asm.keys())[key_index + i]
            text = self.asm[key]
            if not i:
               a = self.font.render(text, True, white, blue) 
            else:  
                a = self.font.render(text, True, green, blue) 

            rect = a.get_rect()
            rect.topleft = (580, 92 + i*15)
            self.surface.blit(a, rect) 


    

    def draw_ram(self):
        starts = [0x0000,0x0008, 0x0010, 0x0018, 0x0020, 0x0028]
        for j, start in enumerate(starts):
            if start < 0x10:
                string = "0x0%s: " %str(hex(start))[-1]
            else:    
                string = "%s: " %hex(start)
            for i in range(0x8):
                
                string += " %s " %str(hex(self.nes.cpuRam[start + i]))[2:]

            
            a = self.font.render(string, True, green, blue)
            rect = a.get_rect()
            rect.topleft = (580, 250 + j*15)
            self.surface.blit(a, rect) 

    def draw_reg(self):

        string = "a: %s    x: %s    y: %s    " %(hex(self.nes.cpu.a), hex(self.nes.cpu.x), hex(self.nes.cpu.y))
            
        a = self.font.render(string, True, green, blue)
        rect = a.get_rect()
        rect.topleft = (580, 380 )
        self.surface.blit(a, rect) 



if __name__ == "__main__":
    screen = Screen()

    screen.turn_on()