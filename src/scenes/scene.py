"""
Scene - Base class for all application scenes
"""
import pygame

class Scene:
    """
    Base scene class that all other scenes inherit from.
    Defines the interface that all scenes must implement.
    """
    
    def initialize(self, surface, config_manager, app_reference=None):
        """
        Initialize the scene
        
        Args:
            surface (pygame.Surface): The surface to render to
            config_manager (ConfigManager): The application configuration manager
            app_reference: Reference to the main application instance
        """
        self.surface = surface
        self.config_manager = config_manager
        self.app = app_reference
        
    def update(self, deltaTime):
        """
        Update scene logic
        
        Args:
            deltaTime (float): Time elapsed since last update in seconds
        """
        pass
        
    def render(self):
        """Render the scene to its surface"""
        pass
        
    def handleEvent(self, event):
        """
        Handle a pygame event
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        pass
        
    def cleanup(self):
        """Clean up any scene resources"""
        pass