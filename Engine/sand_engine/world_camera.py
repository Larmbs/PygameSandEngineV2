"""
Templace for basic world camera to be uesd in game scene
"""
class WorldCamera:
    def __init__(self, window_res, x, y, zoom):
        self.res = window_res
        self.x = x
        self.y = y
        self.zoom = zoom
        