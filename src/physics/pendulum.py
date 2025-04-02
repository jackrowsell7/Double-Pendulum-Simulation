"""
Pendulum - Core physics implementation for a double pendulum
"""
import pygame
import math
from src.physics.path_tracer import PathTracer

class Pendulum:
    """
    Implements the physics of a double pendulum system.
    Handles updating physics state, rendering, and user interaction.
    """
    
    def __init__(self):
        """Initialize the pendulum with default values"""
        # Unique identifier
        self.id = -1
        
        # Anchor point
        self.offsetX = 0
        self.offsetY = 0
        
        # Physical parameters
        self.length1 = 100  # Length of first pendulum arm (pixels)
        self.length2 = 100  # Length of second pendulum arm (pixels)
        self.mass1 = 10     # Mass of first pendulum bob
        self.mass2 = 10     # Mass of second pendulum bob
        
        # Dynamic state
        self.angle1 = 0     # Angle of first pendulum (radians)
        self.angle2 = 0     # Angle of second pendulum (radians)
        self.vel1 = 0       # Angular velocity of first pendulum
        self.vel2 = 0       # Angular velocity of second pendulum
        
        # Initial state for reset
        self.initial_angle1 = 0
        self.initial_angle2 = 0
        
        # Visual parameters
        self.showWire = True
        self.wireColor = pygame.Color(200, 200, 200)
        self.bobColor1 = pygame.Color(220, 50, 50)
        self.bobColor2 = pygame.Color(50, 50, 220)
        self.selectedColor = pygame.Color(150, 255, 150)
        self.bobRadius1 = 10
        self.bobRadius2 = 10
        
        # UI state
        self.draggingBob = 0  # 0: not dragging, 1: first bob, 2: second bob
        
        # Path tracing
        self.pathTracer = None
        
    def initialize(self, params):
        """
        Initialize the pendulum with provided parameters
        
        Args:
            params (PendulumParams): Parameters for initialization
        """
        # Set position
        self.offsetX = params.offsetX
        self.offsetY = params.offsetY
        
        # Set physical parameters
        self.length1 = params.length1
        self.length2 = params.length2
        self.mass1 = params.mass1
        self.mass2 = params.mass2
        
        # Set dynamic state
        self.angle1 = params.angle1
        self.angle2 = params.angle2
        self.vel1 = params.velocity1
        self.vel2 = params.velocity2
        
        # Save initial state for reset
        self.initial_angle1 = params.angle1
        self.initial_angle2 = params.angle2
        
        # Set visual parameters
        self.showWire = params.showWire
        
        # Create path tracer
        self.pathTracer = PathTracer()
        self.pathTracer.initialize(
            params.pathColor,
            params.pathDuration
        )
        
    def reset(self):
        """Reset the pendulum to its initial state"""
        self.angle1 = self.initial_angle1
        self.angle2 = self.initial_angle2
        self.vel1 = 0
        self.vel2 = 0
        
        # Clear path tracer
        if self.pathTracer:
            self.pathTracer.clear()
        
    def update(self, deltaTime, gravity):
        """
        Update pendulum physics
        
        Args:
            deltaTime (float): Time elapsed since last update in seconds
            gravity (float): Current gravity value
        """
        # Don't update physics if dragging
        if self.draggingBob > 0:
            return
            
        # Calculate new angles and velocities using physics equations
        
        # Equations for double pendulum motion, using the Lagrangian formulation
        # These equations are complex but accurately model the chaos of a double pendulum
        
        # Common terms to avoid recalculation
        sin1 = math.sin(self.angle1)
        sin2 = math.sin(self.angle2)
        cos1 = math.cos(self.angle1)
        cos2 = math.cos(self.angle2)
        sin12 = math.sin(self.angle1 - self.angle2)
        cos12 = math.cos(self.angle1 - self.angle2)
        
        # Computing acceleration terms
        m1 = self.mass1
        m2 = self.mass2
        l1 = self.length1
        l2 = self.length2
        
        # First calculate numerators and denominator for the accelerations
        # For angle1 acceleration
        num1 = -gravity * (2 * m1 + m2) * sin1
        num1 -= m2 * gravity * math.sin(self.angle1 - 2 * self.angle2)
        num1 -= 2 * sin12 * m2 * (self.vel2**2 * l2 + self.vel1**2 * l1 * cos12)
        
        # For angle2 acceleration
        num2 = 2 * sin12
        num2 *= (self.vel1**2 * l1 * (m1 + m2) + gravity * (m1 + m2) * cos1)
        num2 += self.vel2**2 * l2 * m2 * cos12
        
        # Common denominator
        den = l1 * (2 * m1 + m2 - m2 * math.cos(2 * (self.angle1 - self.angle2)))
        
        # Compute accelerations using derived equations
        acc1 = num1 / den
        acc2 = num2 / (l2 * den)
        
        # Update velocities using Euler integration
        self.vel1 += acc1 * deltaTime
        self.vel2 += acc2 * deltaTime
        
        # Update angles using velocities
        self.angle1 += self.vel1 * deltaTime
        self.angle2 += self.vel2 * deltaTime
        
        # Update path tracing
        if self.pathTracer:
            p2x, p2y = self._calculate_bob2_position()
            self.pathTracer.addPoint(p2x, p2y, deltaTime)
    
    def render(self, surface):
        """
        Render the pendulum to the surface
        
        Args:
            surface (pygame.Surface): Surface to render to
        """
        # Calculate positions of pendulum bobs
        p1x = self.offsetX + int(self.length1 * math.sin(self.angle1))
        p1y = self.offsetY + int(self.length1 * math.cos(self.angle1))
        
        p2x = p1x + int(self.length2 * math.sin(self.angle2))
        p2y = p1y + int(self.length2 * math.cos(self.angle2))
        
        # Draw path trace if available
        if self.pathTracer:
            self.pathTracer.render(surface)
        
        # Draw pendulum wires if enabled
        if self.showWire:
            pygame.draw.line(surface, self.wireColor, (self.offsetX, self.offsetY), (p1x, p1y), 2)
            pygame.draw.line(surface, self.wireColor, (p1x, p1y), (p2x, p2y), 2)
        
        # Draw pendulum bobs (circles)
        # Determine colors based on dragging state
        bob1_color = self.selectedColor if self.draggingBob == 1 else self.bobColor1
        bob2_color = self.selectedColor if self.draggingBob == 2 else self.bobColor2
        
        # Draw first bob
        pygame.draw.circle(surface, bob1_color, (p1x, p1y), self.bobRadius1)
        
        # Draw second bob
        pygame.draw.circle(surface, bob2_color, (p2x, p2y), self.bobRadius2)
    
    def startDrag(self, mousePos):
        """
        Start dragging a pendulum bob if mouse is over it
        
        Args:
            mousePos (tuple): Mouse position (x, y)
            
        Returns:
            bool: True if dragging started, False otherwise
        """
        # Calculate positions of pendulum bobs
        p1x, p1y = self._calculate_bob1_position()
        p2x, p2y = self._calculate_bob2_position()
        
        # Check if mouse is over second bob first (should take precedence if overlapping)
        dx = mousePos[0] - p2x
        dy = mousePos[1] - p2y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist <= self.bobRadius2:
            self.draggingBob = 2
            return True
        
        # Check if mouse is over first bob
        dx = mousePos[0] - p1x
        dy = mousePos[1] - p1y
        dist = math.sqrt(dx*dx + dy*dy)
        
        if dist <= self.bobRadius1:
            self.draggingBob = 1
            return True
            
        return False
    
    def updateDrag(self, mousePos):
        """
        Update pendulum position during drag
        
        Args:
            mousePos (tuple): New mouse position (x, y)
        """
        if self.draggingBob == 1:
            # Calculate new angle for first pendulum
            dx = mousePos[0] - self.offsetX
            dy = mousePos[1] - self.offsetY
            self.angle1 = math.atan2(dx, dy)
            
            # Reset velocity
            self.vel1 = 0
            
        elif self.draggingBob == 2:
            # First calculate position of bob 1
            p1x, p1y = self._calculate_bob1_position()
            
            # Calculate new angle for second pendulum
            dx = mousePos[0] - p1x
            dy = mousePos[1] - p1y
            self.angle2 = math.atan2(dx, dy)
            
            # Reset velocity
            self.vel2 = 0
    
    def endDrag(self):
        """End drag operation"""
        self.draggingBob = 0
    
    def toggleWireVisibility(self):
        """Toggle wire visibility"""
        self.showWire = not self.showWire
        
    def _calculate_bob1_position(self):
        """
        Calculate position of first pendulum bob
        
        Returns:
            tuple: (x, y) position of first bob
        """
        p1x = self.offsetX + int(self.length1 * math.sin(self.angle1))
        p1y = self.offsetY + int(self.length1 * math.cos(self.angle1))
        return (p1x, p1y)
    
    def _calculate_bob2_position(self):
        """
        Calculate position of second pendulum bob
        
        Returns:
            tuple: (x, y) position of second bob
        """
        p1x, p1y = self._calculate_bob1_position()
        p2x = p1x + int(self.length2 * math.sin(self.angle2))
        p2y = p1y + int(self.length2 * math.cos(self.angle2))
        return (p2x, p2y)