"""
PendulumSystem - Manages a collection of pendulums in the simulation
"""
import pygame
from src.physics.pendulum import Pendulum

class PendulumSystem:
    """
    Manages a collection of pendulum objects for the simulation.
    Handles their creation, updates, and rendering.
    """
    
    def __init__(self):
        """Initialize the pendulum system"""
        # Collection of pendulums
        self.pendulums = []
        
        # Next available pendulum ID
        self.next_id = 0
        
        # Dragging state
        self.dragging_pendulum = None
        
        # Physics settings
        self.gravity = 9.8
        self.time_scale = 1.0
        self.paused = True
    
    def createPendulum(self, params):
        """
        Create a new pendulum with the given parameters
        
        Args:
            params: The parameters for the new pendulum
            
        Returns:
            int: The ID of the new pendulum
        """
        # Create a new pendulum
        pendulum = Pendulum()
        
        # Assign a unique ID
        pendulum.id = self.next_id
        self.next_id += 1
        
        # Initialize with parameters
        pendulum.initialize(params)
        
        # Add to collection
        self.pendulums.append(pendulum)
        
        # Return the ID
        return pendulum.id
    
    def removePendulum(self, pendulum_id):
        """
        Remove a pendulum by ID
        
        Args:
            pendulum_id (int): The ID of the pendulum to remove
            
        Returns:
            bool: True if the pendulum was removed, False if not found
        """
        for i, pendulum in enumerate(self.pendulums):
            if pendulum.id == pendulum_id:
                del self.pendulums[i]
                return True
        
        return False
    
    def getPendulum(self, pendulum_id):
        """
        Get a pendulum by ID
        
        Args:
            pendulum_id (int): The ID of the pendulum to retrieve
            
        Returns:
            Pendulum: The pendulum object, or None if not found
        """
        for pendulum in self.pendulums:
            if pendulum.id == pendulum_id:
                return pendulum
        
        return None
    
    def update(self, deltaTime):
        """
        Update all pendulums
        
        Args:
            deltaTime (float): Time elapsed since last update in seconds
        """
        # Skip update if paused
        if self.paused:
            return
        
        # Scale time
        scaled_dt = deltaTime * self.time_scale
        
        # Update all pendulums
        for pendulum in self.pendulums:
            pendulum.update(scaled_dt, self.gravity)
    
    def render(self, surface):
        """
        Render all pendulums
        
        Args:
            surface (pygame.Surface): Surface to render to
        """
        for pendulum in self.pendulums:
            pendulum.render(surface)
    
    def handleMouseDown(self, pos):
        """
        Handle mouse down event for dragging pendulums
        
        Args:
            pos (tuple): Mouse position (x, y)
            
        Returns:
            bool: True if a pendulum was grabbed, False otherwise
        """
        # Try to grab pendulums in reverse order (last added first)
        for pendulum in reversed(self.pendulums):
            if pendulum.startDrag(pos):
                self.dragging_pendulum = pendulum
                return True
        
        return False
    
    def handleMouseMove(self, pos):
        """
        Handle mouse move event for dragging pendulums
        
        Args:
            pos (tuple): New mouse position (x, y)
        """
        if self.dragging_pendulum:
            self.dragging_pendulum.updateDrag(pos)
    
    def handleMouseUp(self):
        """Handle mouse up event for dragging pendulums"""
        if self.dragging_pendulum:
            self.dragging_pendulum.endDrag()
            self.dragging_pendulum = None
    
    def resetAll(self):
        """Reset all pendulums to their initial state"""
        for pendulum in self.pendulums:
            pendulum.reset()
    
    def setPaused(self, paused):
        """
        Set the paused state
        
        Args:
            paused (bool): Whether the simulation should be paused
        """
        self.paused = paused
    
    def setGravity(self, gravity):
        """
        Set the gravity value
        
        Args:
            gravity (float): The gravity value to use
        """
        self.gravity = gravity
    
    def setTimeScale(self, scale):
        """
        Set the time scale
        
        Args:
            scale (float): The time scale factor
        """
        self.time_scale = scale
    
    def toggleWireVisibility(self, pendulum_id):
        """
        Toggle wire visibility for a pendulum
        
        Args:
            pendulum_id (int): The ID of the pendulum
            
        Returns:
            bool: True if successful, False if pendulum not found
        """
        pendulum = self.getPendulum(pendulum_id)
        if pendulum:
            pendulum.toggleWireVisibility()
            return True
        
        return False