import pygame
from bus import Bus
from Cartridge import Cartridge
import numpy as np

white = (255, 255, 255) 
green = (0, 255, 0) 
blue = (0, 0, 128) 

class Screen:

    def __init__(self):
        pygame.init()

        """
        Sets up NES
        """
        self.nes = Bus()
        self.cart = Cartridge("../Roms/nestest.nes")
        self.nes.insertCartridge(self.cart)
        self.asm = self.nes.cpu.disassemble(0x0000, 0xFFFF)
        #self.nes.cpu.pc = 0xC000
        self.nes.reset()
        #self.asm = self.nes.load_test()

        self.bEmulationRun = False
        self.fResidualTime = 0.0

        self.x = 800
        self.y = 480

        self.surface = pygame.display.set_mode((self.x,self.y))
        self.font = pygame.font.Font('freesansbold.ttf', 15)

        """
        Starts NES
        """

        

        
        """
        Sets caption...
        """
        pygame.display.set_caption("pyNES")

    
    def turn_on(self):
        t = pygame.time.get_ticks()
        getTicksLastFrame = t
        self.total = 0
        self.dt = 0
        while True:
            t = pygame.time.get_ticks()
            deltaTime = (t - getTicksLastFrame) / 1000.0
            getTicksLastFrame = t
            self.dt = deltaTime
            self.total += deltaTime


            self.surface.fill(blue)
            self.draw_code()
            self.draw_ram()
            self.draw_reg()

            self.draw_screen()

            if self.bEmulationRun:
                if (self.fResidualTime > 0.0):
                    self.fResidualTime -= deltaTime
                else:
                
                    self.fResidualTime += (1.0 / 60.0) - deltaTime
                    k = t
                    while True: 
                        self.nes.clock()
                        
                        if self.nes.ppu.frame_complete:
                            break

                    self.dt = (k - pygame.time.get_ticks())/1000
                    self.nes.ppu.frame_complete = False
            for event in pygame.event.get() :
                    if event.type == pygame.QUIT : 
                        pygame.quit()  
                        quit() 
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            k = t
                            while True: 
                                self.nes.clock()
                                
                                if self.nes.ppu.frame_complete:
                                    break
                            self.nes.ppu.frame_complete = False
                            print((k - pygame.time.get_ticks())/1000)

                        if event.key == pygame.K_r:
                            self.nes.reset()

                        if event.key == pygame.K_SPACE:
                            self.bEmulationRun = not self.bEmulationRun
                            
                            
            
                
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

        string = " time: %.3f dt: %.6f" %(self.total, self.dt)
        a = self.font.render(string, True, green, blue)
        rect = a.get_rect()
        rect.topleft = (580, 390 )
        self.surface.blit(a, rect)  


    def draw_screen(self):
        sprite = self.nes.ppu.GetScreen()
        
        sprite_size = sprite[:,:,0].shape
        
        for i in range(int(sprite_size[0])):
            for j in range(int(sprite_size[1])):
                x = 2*i
                y = 2*j
                self.surface.set_at((x,y), sprite[i,j,:])
                self.surface.set_at((x+1,y), sprite[i,j,:])
                self.surface.set_at((x,y+1), sprite[i,j,:])
                self.surface.set_at((x+1,y+1), sprite[i,j,:])



if __name__ == "__main__":
    screen = Screen()

    screen.turn_on()