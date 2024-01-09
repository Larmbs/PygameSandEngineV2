import numpy as np
import numba

"""
This code if purely meant to be structural 
other classes are respinsible for drawing, creating, loading and saving world instances

***Only data storage classes no simulation or drawing***
"""


"""
Small Storage device for world data 
Stored as np.ndarray and has basic helper methods
size is usually 16x16
"""
class Chunk:
    def __init__(self, size:int):
        self.size = size
        self.data = np.zeros((self.size, self.size), dtype=np.int8)
        
    def get_id(self, local_x:int, local_y:int) -> int:
        return self.data[local_x, local_y]
    
    def set_id(self, local_x:int, local_y:int, new_id:int) -> None:
        self.data[local_x, local_y] = new_id
                
    def get_data(self) -> np.ndarray:
        return self.data

"""
Basic World object holds all pixel data in the form of chunks
chunks are stored in form of dictinary
default chunk is blank
"""
class World:
    chunkSize:int = 32
    
    def __init__(self):
        self.world_data:dict[str, Chunk] = {}
        self.default = Chunk(self.chunkSize)
        
    def get_chunk(self, x:int, y:int) -> Chunk:
        return self.world_data.get(f"{int(x)},{int(y)}", None)
    
    def add_chunk(self, x:int, y:int, chunk:Chunk) -> None:
        self.world_data[f"{int(x)},{int(y)}"] = chunk
    
    """Returns tuple[] conating local pos <tuple[int, int]> and chunk pos <tuple[int, int]>"""
    def get_local_and_chunk_pos(self, world_x:int, world_y:int) -> tuple[tuple[int, int], tuple[int, int]]:
        chunk_x, local_x = divmod(world_x, self.chunkSize)
        chunk_y, local_y = divmod(world_y, self.chunkSize)
        return (local_x, local_y), (chunk_x, chunk_y)
    
    def get_id_at_cor(self, world_x:int, world_y:int) -> int:
        position = self.get_local_and_chunk_pos(world_x, world_y)
        chunk = self.get_chunk(*position[1])
        return chunk.get_id(*position[0])
    
    def set_id_at_cor(self, world_x:int, world_y:int, new_id:int) -> int:
        position = self.get_local_and_chunk_pos(world_x, world_y)
        chunk = self.get_chunk(*position[1])
        chunk.set_id(*position[0], new_id)
    