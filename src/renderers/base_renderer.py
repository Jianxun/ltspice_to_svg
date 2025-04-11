from abc import ABC
import logging
import svgwrite

class BaseRenderer(ABC):
    def __init__(self, dwg: svgwrite.Drawing):
        self.dwg = dwg
        self.logger = logging.getLogger(self.__class__.__name__) 