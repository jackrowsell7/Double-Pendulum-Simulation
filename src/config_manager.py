"""
ConfigManager - Handles application configuration settings and theme management
"""
import os
import json

class ConfigManager:
    """
    Manages application configuration, storing user settings and handling
    theme switching.
    """
    
    def __init__(self):
        """Initialize the ConfigManager with default values"""
        self.settings = {
            "theme": "light",  # Default theme (light/dark)
            "gravity": 9.81,   # Default gravity in m/s^2
            "simulation_speed": 1.0,  # Default simulation speed multiplier
            "path_duration": 2.0,     # Default path duration in seconds
            "path_color": [50, 100, 200],  # Default path color (RGB)
            "show_wire": True,        # Whether to show pendulum wire
            "fps_limit": 60           # Frame rate limit
        }
        self.configFilePath = ""
        
    def initialize(self, filePath):
        """
        Initialize the configuration manager
        
        Args:
            filePath (str): Path to the configuration file
        """
        self.configFilePath = filePath
        self.loadConfiguration()
        
    def loadConfiguration(self):
        """
        Load settings from the configuration file
        
        Returns:
            bool: True if loading was successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.configFilePath), exist_ok=True)
            
            # If the file exists, load it
            if os.path.exists(self.configFilePath):
                with open(self.configFilePath, 'r') as f:
                    loaded_settings = json.load(f)
                    # Update settings with loaded values
                    self.settings.update(loaded_settings)
                return True
            else:
                # Create default configuration file
                self.saveConfiguration()
                return True
        except Exception as e:
            print(f"Error loading configuration: {e}")
            return False
            
    def saveConfiguration(self):
        """
        Save current settings to the configuration file
        
        Returns:
            bool: True if saving was successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.configFilePath), exist_ok=True)
            
            # Save settings to file
            with open(self.configFilePath, 'w') as f:
                json.dump(self.settings, f, indent=4)
            return True
        except Exception as e:
            print(f"Error saving configuration: {e}")
            return False
            
    def getSetting(self, key):
        """
        Get a setting value by key
        
        Args:
            key (str): The setting key to look up
            
        Returns:
            object: The setting value or None if key not found
        """
        return self.settings.get(key)
        
    def setSetting(self, key, value):
        """
        Set a setting value
        
        Args:
            key (str): The setting key to set
            value (object): The value to set
            
        Returns:
            bool: True if successful, False otherwise
        """
        self.settings[key] = value
        return True
        
    def applyTheme(self, themeName):
        """
        Apply a specific theme to the application
        
        Args:
            themeName (str): The theme name to apply (light/dark)
            
        Returns:
            dict: Dictionary of theme colors and properties
        """
        # Set the theme name in settings
        self.setSetting("theme", themeName)
        
        # Define color schemes for different themes
        themes = {
            "light": {
                "background": (240, 240, 245),
                "text": (20, 20, 20),
                "button": (200, 200, 210),
                "button_hover": (180, 180, 200),
                "button_text": (20, 20, 20),
                "pendulum_bob": (50, 50, 150),
                "pendulum_wire": (100, 100, 100),
                "grid": (200, 200, 210)
            },
            "dark": {
                "background": (30, 30, 40),
                "text": (220, 220, 220),
                "button": (60, 60, 80),
                "button_hover": (80, 80, 100),
                "button_text": (220, 220, 220),
                "pendulum_bob": (100, 150, 250),
                "pendulum_wire": (180, 180, 180),
                "grid": (50, 50, 60)
            }
        }
        
        # Return the appropriate color scheme
        return themes.get(themeName, themes["light"])