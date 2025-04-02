"""
PendulumParams - Parameter container for initializing pendulum objects
"""
import pygame
import math

class PendulumParams:
    """
    Container class for pendulum initialization parameters.
    Handles all the parameters needed to create and configure a pendulum.
    """
    
    def __init__(self):
        """Initialize pendulum parameters with default values"""
        # Position
        self.offsetX = 400
        self.offsetY = 100
        
        # Physical parameters
        self.length1 = 120
        self.length2 = 120
        self.mass1 = 10
        self.mass2 = 10
        
        # Initial state
        self.angle1 = math.pi / 4  # 45 degrees
        self.angle2 = math.pi / 4  # 45 degrees
        self.velocity1 = 0.0
        self.velocity2 = 0.0
        
        # Visual parameters
        self.showWire = True
        self.pathColor = pygame.Color(80, 180, 255)
        self.pathDuration = 5.0  # seconds
        
    def randomize(self):
        """Generate random parameter values for creating varied pendulums"""
        import random
        
        # Randomize angles (keep them within reasonable limits)
        self.angle1 = random.uniform(-math.pi/2, math.pi/2)
        self.angle2 = random.uniform(-math.pi/2, math.pi/2)
        
        # Randomize lengths (keep them within reasonable limits)
        self.length1 = random.randint(80, 150)
        self.length2 = random.randint(80, 150)
        
        # Randomize masses
        self.mass1 = random.randint(5, 15)
        self.mass2 = random.randint(5, 15)
        
        # Randomize path color
        r = random.randint(20, 255)
        g = random.randint(20, 255)
        b = random.randint(20, 255)
        self.pathColor = pygame.Color(r, g, b)
        
    def clone(self):
        """
        Create a copy of this parameter set
        
        Returns:
            PendulumParams: A new parameter object with the same values
        """
        params = PendulumParams()
        
        # Copy all parameter values
        params.offsetX = self.offsetX
        params.offsetY = self.offsetY
        params.length1 = self.length1
        params.length2 = self.length2
        params.mass1 = self.mass1
        params.mass2 = self.mass2
        params.angle1 = self.angle1
        params.angle2 = self.angle2
        params.velocity1 = self.velocity1
        params.velocity2 = self.velocity2
        params.showWire = self.showWire
        params.pathColor = pygame.Color(
            self.pathColor.r,
            self.pathColor.g,
            self.pathColor.b
        )
        params.pathDuration = self.pathDuration
        
        return params