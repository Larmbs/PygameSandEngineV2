import pygame as pg
from .world import World
from .world_camera import WorldCamera
from .matrix_to_surface import chunk_to_surf

"""
This File has one responsibility
***Only display the world given camera information***

Process
First determines objects that will be in world view
Next converts the chunk data to pg.Surface objects
Next determines correct transformations to those surface
Finally displays those to the world screen 
"""

"""Width, Height of rectangle"""
VIEW_RECT = tuple[int, int]
""""""
Rect = tuple[int, int, int, int]

def scale_relative(surface:pg.Surface, scalar:float):
    original_size = surface.get_size()
    new_size = (int(original_size[0] * scalar), int(original_size[1] * scalar))
    return pg.transform.scale(surface, new_size)

"""Class purely responsible for handing what chunks to render for user"""
class WorldRenderer:
    def __init__(self, world:World, camera:WorldCamera):
        self.world = world
        self.camera = camera
        self.world_screen = pg.Surface(self.camera.res)
        self.chunks_rendered = 0
    
    """Returns rectangle of chunks in view and offset"""
    def update(self):
        self.block_size = self.camera.zoom * 4
        self.world_space_width = self.camera.res[0]/self.block_size - 20
        self.world_space_height = self.camera.res[1]/self.block_size - 20
    
    def get_chunks_in_view(self) -> tuple[VIEW_RECT, tuple[float, float]]:
        self.update()
        
        needed_horz_chunks, offset_x = divmod(self.world_space_width, self.world.chunkSize)
        needed_vert_chunks, offset_y = divmod(self.world_space_height, self.world.chunkSize)
        offset_x += self.camera.x
        offset_y += self.camera.y
        chunk_offset_x, offset_x = divmod(offset_x, self.world.chunkSize)
        chunk_offset_y, offset_y = divmod(offset_y, self.world.chunkSize)
        
        return (int(needed_horz_chunks) + 2, int(needed_vert_chunks) + 2), (chunk_offset_x, chunk_offset_y), (offset_x, offset_y)
        
    def draw_chunks_to_world_surf(self, view_rect:VIEW_RECT, chunkOff, offset:tuple[float, float]):
        combined_surf = pg.Surface((view_rect[0]*self.world.chunkSize, view_rect[1]*self.world.chunkSize))
        for x_index in range(view_rect[0]):
            for y_index in range(view_rect[1]):
                self.draw_chunk_to_world_surf(combined_surf, int(x_index), int(y_index), chunkOff)
        self.world_screen.blit(scale_relative(combined_surf, self.block_size), (offset[0]*self.block_size - self.world.chunkSize*self.block_size, offset[1]*self.block_size - self.world.chunkSize*self.block_size))
    
    def draw_chunk_to_world_surf(self, surface:pg.Surface, x_index:int, y_index:int, offset):
        chunk = self.world.get_chunk(x_index-offset[0], y_index-offset[1])
        if chunk is not None:
            chunk_surf = chunk_to_surf(chunk)
            self.chunks_rendered += 1
            surface.blit(chunk_surf, ((x_index) * self.world.chunkSize, (y_index) * self.world.chunkSize))
                
    def update_view(self):
        self.chunks_rendered = 0
        chunks_to_render = self.get_chunks_in_view()
        self.draw_chunks_to_world_surf(chunks_to_render[0], chunks_to_render[1], chunks_to_render[2])
                
    def get_screen(self) -> pg.Surface:
        return self.world_screen
    