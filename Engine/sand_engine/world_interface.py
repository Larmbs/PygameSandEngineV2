from .world import World
from .world_manager import WorldManager
import pygame as pg
import numpy as np
from .surface_handler import WorldRenderer
from .world_camera import WorldCamera
        
"""
Responsible for handling user requests and enacting right methods on world
"""

class WorldInterface:
    def __init__(self, world:World, window_res):
        self.world = world
        self.world_camera = WorldCamera(window_res, 0, 0, 2)
        self.renderer = WorldRenderer(self.world, self.world_camera)
        self.manager = WorldManager(self.world)
        
    def update(self):
        self.manager.update()
        self.renderer.update_view()
    
    def get_screen(self) -> pg.Surface:
        return self.renderer.get_screen()