import numba
import numpy as np
from .materials import get_color
from .world import Chunk
import pygame as pg

@numba.njit()
def convert_ids_to_col(matrix_ids:np.ndarray) -> np.ndarray:
    rows, cols = matrix_ids.shape
    result = np.empty((rows, cols, 3), dtype=np.uint8)
    for i in range(rows):
        for j in range(cols):
            result[i, j, :] = get_color(matrix_ids[i, j])
    return result

def convert_col_matrix_to_surf(color_matrix:np.ndarray) -> pg.Surface:
    surf = pg.Surface((color_matrix.shape[0], color_matrix.shape[1]))
    pg.surfarray.blit_array(surf, color_matrix)
    return surf

def chunk_to_surf(chunk:Chunk):
    color_matrix = convert_ids_to_col(chunk.get_data())
    surface = convert_col_matrix_to_surf(color_matrix)
    return surface