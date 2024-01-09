from abc import ABC, abstractmethod
from .world import World, Chunk
import numpy as np
import numba
import time
from opensimplex import OpenSimplex

"""Template for world creation class"""
class Generator(ABC):
    chunk_size:int = 32
    
    def __init__(self, horz_chunks, vert_chunks):
        self.chunks_horz = horz_chunks
        self.chunks_vert = vert_chunks
        self.world = World()
        
    def create_chunks(self):
        for x in range(self.chunks_horz):
            for y in range(self.chunks_vert):
                chunk = Chunk(self.chunk_size)
                self.world.add_chunk(x, y, chunk)
    
    def generate_chunks(self):
        for x in range(self.chunks_horz):
            for y in range(self.chunks_vert):
                self.generate_chunk(x*self.chunk_size, y*self.chunk_size)
    
    def generate_chunk(self, x_off, y_off):
        for x in range(self.chunk_size):
            for y in range(self.chunk_size):
                self.world.set_id_at_cor(x_off+x, y_off+y, self.algo(x_off+x, y_off+y))
                
    def generate(self):
        start = time.perf_counter()
        self.create_chunks()
        self.generate_chunks()
        end = time.perf_counter()
        print(f"Time was {np.floor(end-start)}")
    
    @abstractmethod
    def algo(self, x:int, y:int) -> int:
        ...
        
    def get_world(self):
        return self.world
    
class Sine(Generator):
    def algo(self, x, y) -> int:
        return perlin_func(x, y)
        
@numba.njit()
def sine_func(x, y):
    if y <= 200 + np.sin(x/10)*50: return 2
    return 1

noise_generator = OpenSimplex(seed=20)
def perlin_func(x, y):
    value = noise_generator.noise2(x/30, y/30)
    if value >= 0.3:return 2
    else:return 1
    