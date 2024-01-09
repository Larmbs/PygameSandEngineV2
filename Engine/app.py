import pygame
from sand_engine import World, WorldInterface, Sine
import sys

class App:
    def __init__(self, WIDTH=1000, HEIGHT=600):
        self.RES = WIDTH, HEIGHT
        pygame.init()
        self.screen = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()
        self.world = Sine(20, 20)
        self.world.generate()
        
        self.game = WorldInterface(self.world.get_world(), self.RES)
        self.move_mult = 1

    def handle_events(self):
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:self.game.renderer.camera.x += self.move_mult
        elif keys_pressed[pygame.K_d]:self.game.renderer.camera.x -= self.move_mult
        
        if keys_pressed[pygame.K_w]:self.game.renderer.camera.y += self.move_mult
        elif keys_pressed[pygame.K_s]:self.game.renderer.camera.y -= self.move_mult
        
        if keys_pressed[pygame.K_z]:self.game.renderer.camera.zoom *= 0.9
        elif keys_pressed[pygame.K_x]:self.game.renderer.camera.zoom *= 1.1
        
        if keys_pressed[pygame.K_LSHIFT]:self.move_mult = 3
        else:self.move_mult = 1
            
    def update(self):
        self.game.update()

    def run(self):
        while True:
            self.handle_events()
            self.update()
            [self.exit() for event in pygame.event.get() if event.type == pygame.QUIT]
            self.screen.blit(self.game.get_screen(), (0,0))
            self.clock.tick()
            pygame.display.set_caption(
            f"Frame Rate: {int(self.clock.get_fps())} FPS |\
              Chunks Rendered: {self.game.renderer.chunks_rendered} |\
              Chunk To Frame Ratio: {int(self.clock.get_fps() / (self.game.renderer.chunks_rendered+1))}")
            pygame.display.flip()


    def exit(self):
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    app = App()
    app.run()
    