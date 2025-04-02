"""
DoublePendulumApp - Main application controller for the Double Pendulum Simulation
"""
import os
import sys
import pygame
import pygame_gui

from src.config_manager import ConfigManager
from src.scene_manager import SceneManager
from src.scenes.home_scene import HomeScene
from src.scenes.simulation_scene import SimulationScene
from src.scenes.settings_scene import SettingsScene
from src.scenes.information_scene import InformationScene

class DoublePendulumApp:
    """
    Main application controller class that manages the application lifecycle,
    scenes, and configuration.
    """
    
    def __init__(self):
        """Initialize the DoublePendulumApp with default values"""
        self.sceneManager = None
        self.configManager = None
        self.mainSurface = None
        self.running = False
        self.clock = None
        self.fps = 60
        
        # Application resolution and title
        self.app_width = 1200
        self.app_height = 800
        self.app_title = "Double Pendulum Simulation"
        
    def initialize(self):
        """Initialize the application, pygame, and all managers"""
        # Initialize pygame modules
        pygame.init()
        pygame.font.init()
        
        # Create the main surface/window
        self.mainSurface = pygame.display.set_mode(
            (self.app_width, self.app_height),
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )
        pygame.display.set_caption(self.app_title)
        
        # Set up the clock for controlling framerate
        self.clock = pygame.time.Clock()
        
        # Initialize the configuration manager
        config_path = os.path.join("data", "config.json")
        self.configManager = ConfigManager()
        self.configManager.initialize(config_path)
        
        # Initialize scene manager
        self.sceneManager = SceneManager()
        self.sceneManager.initialize()
        
        # Register scenes
        self._register_scenes()
        
        # Change to the home scene
        self.sceneManager.changeScene("home")
        
        # Mark as running
        self.running = True
        
    def _register_scenes(self):
        """Register all application scenes with the scene manager"""
        print("Registering scenes...")
        
        # Create and register the home scene
        home_scene = HomeScene()
        home_scene.initialize(self.mainSurface, self.configManager, self)
        self.sceneManager.registerScene("home", home_scene)
        print("Registered: home")
        
        # Create and register the simulation scene
        try:
            simulation_scene = SimulationScene()
            simulation_scene.initialize(self.mainSurface, self.configManager, self)
            self.sceneManager.registerScene("simulation", simulation_scene)
            print("Registered: simulation")
        except Exception as e:
            print(f"Error registering simulation scene: {e}")
            import traceback
            traceback.print_exc()
        
        # Create and register the settings scene
        settings_scene = SettingsScene()
        settings_scene.initialize(self.mainSurface, self.configManager, self)
        self.sceneManager.registerScene("settings", settings_scene)
        print("Registered: settings")
        
        # Create and register the information scene
        info_scene = InformationScene()
        info_scene.initialize(self.mainSurface, self.configManager, self)
        self.sceneManager.registerScene("information", info_scene)
        print("Registered: information")
        
    def run(self):
        """Run the main application loop"""
        while self.running:
            # Calculate delta time in seconds
            delta_time = self.clock.tick(self.fps) / 1000.0
            
            # Process events
            for event in pygame.event.get():
                # Handle quit event
                if event.type == pygame.QUIT:
                    self.running = False
                    break
                
                # Let the current scene handle the event
                self.sceneManager.getCurrentScene().handleEvent(event)
            
            # Update the current scene
            self.sceneManager.getCurrentScene().update(delta_time)
            
            # Render the current scene
            self.sceneManager.getCurrentScene().render()
            
            # Update the display
            pygame.display.flip()
    
    def exit(self):
        """Clean up resources and exit the application"""
        # Clean up current scene
        if self.sceneManager and self.sceneManager.getCurrentScene():
            self.sceneManager.getCurrentScene().cleanup()
        
        # Save configuration
        if self.configManager:
            self.configManager.saveConfiguration()
        
        # Quit pygame
        pygame.quit()
        
        # Exit the application
        sys.exit(0)