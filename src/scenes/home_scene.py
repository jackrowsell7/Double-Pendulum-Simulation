"""
HomeScene - Main menu scene for the Double Pendulum Simulation
"""
import pygame
import pygame_gui
from src.scenes.scene import Scene

class HomeScene(Scene):
    """
    The main menu scene that provides navigation to other parts of the application.
    Displays a welcoming interface with buttons to access different features.
    """
    
    def initialize(self, surface, config_manager, app_reference=None):
        """
        Initialize the home scene
        
        Args:
            surface (pygame.Surface): The surface to render to
            config_manager (ConfigManager): The application configuration manager
            app_reference: Reference to the main application instance
        """
        # Call the parent class initialize method
        super().initialize(surface, config_manager, app_reference)
        
        # Get screen dimensions
        self.width, self.height = self.surface.get_size()
        
        # Create UI manager
        self.ui_manager = pygame_gui.UIManager((self.width, self.height))
        
        # Apply theme colors
        theme_colors = self.config_manager.applyTheme(
            self.config_manager.getSetting("theme")
        )
        self.bg_color = theme_colors["background"]
        self.text_color = theme_colors["text"]
        
        # Create app title font
        self.title_font = pygame.font.SysFont('Arial', 64, bold=True)
        self.subtitle_font = pygame.font.SysFont('Arial', 24)
        
        # Create buttons
        self._create_ui_elements()
        
    def _create_ui_elements(self):
        """Create all UI elements for the home scene"""
        # Calculate button dimensions and positions
        button_width = 250
        button_height = 60
        padding = 20
        start_y = self.height // 2 - 50
        
        # Create simulation button
        self.simulation_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.width // 2 - button_width // 2, start_y),
                (button_width, button_height)
            ),
            text='Start Simulation',
            manager=self.ui_manager
        )
        
        # Create settings button
        self.settings_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.width // 2 - button_width // 2, start_y + button_height + padding),
                (button_width, button_height)
            ),
            text='Settings',
            manager=self.ui_manager
        )
        
        # Create information button
        self.info_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.width // 2 - button_width // 2, start_y + 2 * (button_height + padding)),
                (button_width, button_height)
            ),
            text='Information',
            manager=self.ui_manager
        )
        
        # Create exit button
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (self.width // 2 - button_width // 2, start_y + 3 * (button_height + padding)),
                (button_width, button_height)
            ),
            text='Exit',
            manager=self.ui_manager
        )
    
    def update(self, deltaTime):
        """
        Update home scene logic
        
        Args:
            deltaTime (float): Time elapsed since last update in seconds
        """
        # Update UI manager
        self.ui_manager.update(deltaTime)
    
    def render(self):
        """Render the home scene to its surface"""
        # Fill background
        self.surface.fill(self.bg_color)
        
        # Render title
        title_surface = self.title_font.render("Double Pendulum", True, self.text_color)
        subtitle_surface = self.subtitle_font.render("A Physics Simulation", True, self.text_color)
        
        title_rect = title_surface.get_rect(centerx=self.width//2, top=self.height//4)
        subtitle_rect = subtitle_surface.get_rect(centerx=self.width//2, top=title_rect.bottom + 10)
        
        self.surface.blit(title_surface, title_rect)
        self.surface.blit(subtitle_surface, subtitle_rect)
        
        # Draw UI elements
        self.ui_manager.draw_ui(self.surface)
    
    def handleEvent(self, event):
        """
        Handle a pygame event
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        # Process event through UI manager
        self.ui_manager.process_events(event)
        
        # Handle button clicks
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.simulation_button:
                    self.handleNavigation("simulation")
                elif event.ui_element == self.settings_button:
                    self.handleNavigation("settings")
                elif event.ui_element == self.info_button:
                    self.handleNavigation("information")
                elif event.ui_element == self.exit_button:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
    
    def handleNavigation(self, destination):
        """
        Handle navigation to another scene
        
        Args:
            destination (str): The name of the scene to navigate to
        """
        print(f"Attempting to navigate to: {destination}")
        # Use the app reference passed during initialization
        if self.app and hasattr(self.app, "sceneManager"):
            print(f"SceneManager exists, navigating to: {destination}")
            result = self.app.sceneManager.changeScene(destination)
            print(f"Scene change result: {result}")
        else:
            print("Failed to access SceneManager")
    
    def cleanup(self):
        """Clean up home scene resources"""
        # Release UI manager resources
        self.ui_manager.clear_and_reset()