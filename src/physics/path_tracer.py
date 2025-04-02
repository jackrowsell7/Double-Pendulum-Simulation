"""
PathTracer - Tracks and renders the path of a pendulum bob over time
"""
import pygame
import numpy as np
from collections import deque
import colorsys

class PathTracer:
    """
    Tracks and renders the path of a pendulum bob over time with a fading effect.
    """
    
    def __init__(self, max_points=1000):
        """
        Initialize the path tracer
        
        Args:
            max_points (int): Maximum number of points to store
        """
        # Trail points stored as deque for efficient appending/popping
        self.points = deque(maxlen=max_points)
        
        # Properties
        self.enabled = True
        self.color = (255, 0, 0)  # Default color (red)
        self.fade_rate = 0.95     # How quickly the trail fades
        self.min_alpha = 10       # Minimum alpha value before removing points
        self.line_thickness = 2   # Thickness of the path line
        
        # Rainbow trail effect
        self.rainbow_mode = False
        self.hue_increment = 0.01
        self.current_hue = 0.0
    
    def clear(self):
        """Clear all stored points"""
        self.points.clear()
    
    def add_point(self, position):
        """
        Add a point to the path
        
        Args:
            position (tuple): (x, y) position to add
        """
        if not self.enabled:
            return
            
        # Store position with full alpha
        x, y = position
        
        # For rainbow mode, generate a color based on current hue
        if self.rainbow_mode:
            r, g, b = colorsys.hsv_to_rgb(self.current_hue, 1.0, 1.0)
            point_color = (int(r * 255), int(g * 255), int(b * 255))
            self.current_hue = (self.current_hue + self.hue_increment) % 1.0
        else:
            point_color = self.color
            
        # Store position, color and full alpha
        self.points.append((x, y, point_color, 255))
    
    def update(self):
        """Update the path tracer (fade points over time)"""
        if not self.points:
            return
            
        # Apply fading to all points
        updated_points = deque(maxlen=self.points.maxlen)
        for x, y, color, alpha in self.points:
            new_alpha = max(int(alpha * self.fade_rate), 0)
            if new_alpha > self.min_alpha:
                updated_points.append((x, y, color, new_alpha))
                
        self.points = updated_points
    
    def render(self, surface):
        """
        Render the path
        
        Args:
            surface (pygame.Surface): Surface to render to
        """
        if not self.enabled or len(self.points) < 2:
            return
            
        # Create a temporary surface for drawing the path
        temp_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        
        # Draw lines between points with their respective alpha values
        for i in range(1, len(self.points)):
            prev_x, prev_y, prev_color, prev_alpha = self.points[i-1]
            x, y, color, alpha = self.points[i]
            
            # Average the alpha between consecutive points
            avg_alpha = (prev_alpha + alpha) // 2
            
            # Use the color of the newer point with the average alpha
            r, g, b = color
            line_color = (r, g, b, avg_alpha)
            
            # Draw the line
            pygame.draw.line(
                temp_surface, 
                line_color,
                (prev_x, prev_y), 
                (x, y),
                self.line_thickness
            )
        
        # Blit the temporary surface onto the main surface
        surface.blit(temp_surface, (0, 0))
    
    def set_color(self, color):
        """
        Set the path color
        
        Args:
            color (tuple): RGB color tuple (r, g, b)
        """
        self.color = color
        
    def toggle_rainbow_mode(self):
        """Toggle the rainbow trail effect"""
        self.rainbow_mode = not self.rainbow_mode
        
    def set_enabled(self, enabled):
        """
        Enable or disable the path tracer
        
        Args:
            enabled (bool): Whether the path tracer should be enabled
        """
        self.enabled = enabled
        
        # Clear points when disabling
        if not enabled:
            self.clear()
            
    def is_enabled(self):
        """
        Check if the path tracer is enabled
        
        Returns:
            bool: Whether the path tracer is enabled
        """
        return self.enabled