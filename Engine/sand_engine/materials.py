from abc import ABC, abstractmethod
import numpy as np
import numba

AIR = 0
RGBA = tuple[int, int, int]

"""
def update(cls, neighbors:list[int]) -> tuple[int, int]:
neighbors is a list of values surrounding the object they ae stored in the following order
bottom_left -> 0
bottom -> 1
bottom_right -> 2
right -> 3
top_right -> 4
top -> 5
top_left -> 6
left -> 7

in total there are eight neighbors

This function determines the particles next location based of realtive data
"""

class Material(ABC):
    color:RGBA
    
    """Given surrounding world data calculates desired outcome"""
    @classmethod
    def update(cls, neighbors:list[int]) -> tuple[int, int]:
        ...
        
class Air(Material):
    color:RGBA=[0, 0, 0]
        
class Sand(Material):
    color:RGBA=[255, 255, 0]
    @classmethod
    def update(cls, neighbors:list[int]) -> tuple[int, int]:
        if neighbors[1] == AIR: return (0, -1)
        elif neighbors[0] == AIR: return (-1, -1)
        elif neighbors[2] == AIR: return (1, -1)
        else: return (0, 0)

class Water(Material):
    color:RGBA=[0, 0, 255]
    @classmethod
    def update(cls, neighbors:list[int]) -> tuple[int, int]:
        if neighbors[1] == AIR: return (0, -1)
        elif neighbors[0] == AIR: return (-1, -1)
        elif neighbors[2] == AIR: return (1, -1)
        elif neighbors[7] == AIR: return (-1, 0)
        elif neighbors[3] == AIR: return (1, 0)
        else: return (0, 0)
    
material_list = np.array([
    Air().color,
    Sand().color,
    Water().color
], dtype=np.uint8)

@numba.njit()
def get_color(block_id:np.uint8) -> RGBA:
    if block_id not in range(0, len(material_list)): block_id = 0
    mat_color = material_list[block_id]
    return mat_color
