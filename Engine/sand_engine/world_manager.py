from .world import World
import numba

"""Wrapper Around World Class to give it functionality"""
"""
Adds physics and manages comupations on world grid and objects
"""
class WorldManager:
    def __init__(self, world:World):
        self.world = world
        
    def update(self):
        self.place_block(100, 100, 1)
        
    def place_block(self, world_x, world_y, id):
        self.world.set_id_at_cor(world_x, world_y, id)

        