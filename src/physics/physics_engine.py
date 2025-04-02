"""
PhysicsEngine - Main physics controller for the pendulum simulation
"""
import pygame
from src.physics.pendulum_system import PendulumSystem
from src.physics.pendulum_params import PendulumParams

class PhysicsEngine:
    """
    Main physics controller for the pendulum simulation.
    Provides a high-level interface to the pendulum system.
    """
    
    def __init__(self):
        """Initialize the physics engine"""
        # Create the pendulum system
        self.pendulum_system = PendulumSystem()
        
        # Default parameter template for creating pendulums
        self.default_params = PendulumParams()
        
        # Time tracking
        self.last_time = 0
        self.accumulated_time = 0
        
        # Physics settings
        self.min_step = 1/240  # Minimum physics step size in seconds
    
    def initialize(self):
        """Initialize the physics engine"""
        # Set up initial configuration
        self.pendulum_system.setGravity(9.81)
        self.pendulum_system.setTimeScale(1.0)
        
        # Create a default pendulum in the center
        params = self.default_params.clone()
        params.offsetX = 400
        params.offsetY = 100
        self.pendulum_system.createPendulum(params)
        
        # Start with simulation paused
        self.pendulum_system.setPaused(True)
        
        # Initialize time tracking
        self.last_time = pygame.time.get_ticks() / 1000.0
    
    def update(self):
        """Update the physics simulation"""
        # Calculate delta time in seconds
        current_time = pygame.time.get_ticks() / 1000.0
        delta_time = current_time - self.last_time
        self.last_time = current_time
        
        # Clamp delta time to avoid large jumps
        if delta_time > 0.1:
            delta_time = 0.1
        
        # Use fixed timestep for physics updates
        self.accumulated_time += delta_time
        
        # Update in fixed steps
        while self.accumulated_time >= self.min_step:
            self.pendulum_system.update(self.min_step)
            self.accumulated_time -= self.min_step
    
    def render(self, surface):
        """
        Render the physics simulation
        
        Args:
            surface (pygame.Surface): Surface to render to
        """
        self.pendulum_system.render(surface)
    
    def addPendulum(self, x=None, y=None):
        """
        Add a new pendulum at the specified position
        
        Args:
            x (int, optional): X position for the pendulum anchor
            y (int, optional): Y position for the pendulum anchor
            
        Returns:
            int: ID of the new pendulum
        """
        params = self.default_params.clone()
        
        # If position provided, use it
        if x is not None and y is not None:
            params.offsetX = x
            params.offsetY = y
        
        # Randomize parameters slightly for variety
        params.randomize()
        
        # Create the pendulum
        return self.pendulum_system.createPendulum(params)
    
    def removePendulum(self, pendulum_id):
        """
        Remove a pendulum by ID
        
        Args:
            pendulum_id (int): ID of the pendulum to remove
            
        Returns:
            bool: True if removed, False if not found
        """
        return self.pendulum_system.removePendulum(pendulum_id)
    
    def resetSimulation(self):
        """Reset all pendulums to their initial state"""
        self.pendulum_system.resetAll()
    
    def setPaused(self, paused):
        """
        Set the paused state of the simulation
        
        Args:
            paused (bool): Whether the simulation should be paused
        """
        self.pendulum_system.setPaused(paused)
    
    def isPaused(self):
        """
        Get the paused state of the simulation
        
        Returns:
            bool: Whether the simulation is currently paused
        """
        return self.pendulum_system.paused
    
    def setGravity(self, gravity):
        """
        Set the gravity value
        
        Args:
            gravity (float): The gravity value (typically 9.81)
        """
        self.pendulum_system.setGravity(gravity)
    
    def setTimeScale(self, scale):
        """
        Set the time scale of the simulation
        
        Args:
            scale (float): Scale factor for simulation speed
        """
        self.pendulum_system.setTimeScale(scale)
    
    def handleMouseDown(self, pos):
        """
        Handle mouse down event
        
        Args:
            pos (tuple): Mouse position (x, y)
            
        Returns:
            bool: True if a pendulum was grabbed, False otherwise
        """
        return self.pendulum_system.handleMouseDown(pos)
    
    def handleMouseMove(self, pos):
        """
        Handle mouse move event
        
        Args:
            pos (tuple): New mouse position (x, y)
        """
        self.pendulum_system.handleMouseMove(pos)
    
    def handleMouseUp(self):
        """Handle mouse up event"""
        self.pendulum_system.handleMouseUp()