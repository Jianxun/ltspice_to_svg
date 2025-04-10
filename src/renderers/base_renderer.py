from abc import ABC, abstractmethod
import logging
import svgwrite

class BaseRenderer(ABC):
    def __init__(self, dwg: svgwrite.Drawing):
        self.dwg = dwg
        self.logger = logging.getLogger(self.__class__.__name__)
        
    @abstractmethod
    def render(self, element: dict) -> None:
        """Render a single element.
        
        Args:
            element (dict): The element to render, containing all necessary properties.
        """
        pass 