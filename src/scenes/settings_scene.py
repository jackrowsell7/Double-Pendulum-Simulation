"""
SettingsScene - Settings configuration scene for the Double Pendulum Simulation
"""
import pygame
import pygame_gui
from src.scenes.scene import Scene

class SettingsScene(Scene):
    """
    Settings scene where users can configure application preferences
    such as theme, default simulation parameters, and display options.
    """
    
    def initialize(self, surface, config_manager, app_reference=None):
        """
        Initialize the settings scene
        
        Args:
            surface (pygame.Surface): The surface to render to
            config_manager (ConfigManager): The application configuration manager
            app_reference: Reference to the main application instance
        """
        # Call parent initialization
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
        
        # Create fonts
        self.title_font = pygame.font.SysFont('Arial', 36)
        self.normal_font = pygame.font.SysFont('Arial', 16)
        
        # Create UI elements
        self._create_ui_elements()
        
    def _create_ui_elements(self):
        """Create all UI elements for the settings scene"""
        # Create panel for settings
        panel_width = 500
        panel_height = 600
        panel_x = self.width // 2 - panel_width // 2
        panel_y = self.height // 2 - panel_height // 2
        
        self.settings_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (panel_x, panel_y),
                (panel_width, panel_height)
            ),
            manager=self.ui_manager
        )
        
        # Title
        title_rect = pygame.Rect(
            (panel_x + 20, panel_y + 20),
            (panel_width - 40, 40)
        )
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=title_rect,
            text="Settings",
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # Theme settings section
        theme_section_rect = pygame.Rect(
            (panel_x + 20, title_rect.bottom + 20),
            (panel_width - 40, 30)
        )
        self.theme_section_label = pygame_gui.elements.UILabel(
            relative_rect=theme_section_rect,
            text="Theme",
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # Light theme button
        light_theme_rect = pygame.Rect(
            (panel_x + 20, theme_section_rect.bottom + 10),
            ((panel_width - 60) // 2, 40)
        )
        self.light_theme_button = pygame_gui.elements.UIButton(
            relative_rect=light_theme_rect,
            text="Light",
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # Dark theme button
        dark_theme_rect = pygame.Rect(
            (light_theme_rect.right + 20, theme_section_rect.bottom + 10),
            ((panel_width - 60) // 2, 40)
        )
        self.dark_theme_button = pygame_gui.elements.UIButton(
            relative_rect=dark_theme_rect,
            text="Dark",
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # Default simulation settings section
        sim_section_rect = pygame.Rect(
            (panel_x + 20, light_theme_rect.bottom + 30),
            (panel_width - 40, 30)
        )
        self.sim_section_label = pygame_gui.elements.UILabel(
            relative_rect=sim_section_rect,
            text="Default Simulation Settings",
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # Default gravity label
        gravity_label_rect = pygame.Rect(
            (panel_x + 20, sim_section_rect.bottom + 15),
            (200, 20)
        )
        self.gravity_label = pygame_gui.elements.UILabel(
            relative_rect=gravity_label_rect,
            text=f"Gravity: {self.config_manager.getSetting('gravity'):.1f} m/s²",
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # Default gravity slider
        gravity_slider_rect = pygame.Rect(
            (gravity_label_rect.right + 10, sim_section_rect.bottom + 15),
            (panel_width - 40 - gravity_label_rect.width - 10, 20)
        )
        self.gravity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=gravity_slider_rect,
            start_value=self.config_manager.getSetting("gravity"),
            value_range=(1.0, 20.0),
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # FPS limit label
        fps_label_rect = pygame.Rect(
            (panel_x + 20, gravity_label_rect.bottom + 15),
            (200, 20)
        )
        self.fps_label = pygame_gui.elements.UILabel(
            relative_rect=fps_label_rect,
            text=f"FPS Limit: {self.config_manager.getSetting('fps_limit')}",
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # FPS limit slider
        fps_slider_rect = pygame.Rect(
            (fps_label_rect.right + 10, gravity_label_rect.bottom + 15),
            (panel_width - 40 - fps_label_rect.width - 10, 20)
        )
        self.fps_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=fps_slider_rect,
            start_value=self.config_manager.getSetting("fps_limit"),
            value_range=(30, 120),
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # Path duration label
        path_label_rect = pygame.Rect(
            (panel_x + 20, fps_label_rect.bottom + 15),
            (200, 20)
        )
        self.path_label = pygame_gui.elements.UILabel(
            relative_rect=path_label_rect,
            text=f"Path Duration: {self.config_manager.getSetting('path_duration'):.1f}s",
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # Path duration slider
        path_slider_rect = pygame.Rect(
            (path_label_rect.right + 10, fps_label_rect.bottom + 15),
            (panel_width - 40 - path_label_rect.width - 10, 20)
        )
        self.path_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=path_slider_rect,
            start_value=self.config_manager.getSetting("path_duration"),
            value_range=(0.5, 10.0),
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # Show wire checkbox label
        wire_label_rect = pygame.Rect(
            (panel_x + 20, path_label_rect.bottom + 15),
            (200, 20)
        )
        self.wire_label = pygame_gui.elements.UILabel(
            relative_rect=wire_label_rect,
            text="Show Pendulum Wire:",
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # Show wire checkbox
        wire_checkbox_rect = pygame.Rect(
            (wire_label_rect.right + 10, path_label_rect.bottom + 15),
            (20, 20)
        )
        self.wire_checkbox = pygame_gui.elements.UIButton(
            relative_rect=wire_checkbox_rect,
            text="✓" if self.config_manager.getSetting("show_wire") else " ",
            manager=self.ui_manager,
            container=self.settings_panel,
            tool_tip_text="Show pendulum connecting wires"
        )
        
        # About section
        about_section_rect = pygame.Rect(
            (panel_x + 20, wire_label_rect.bottom + 30),
            (panel_width - 40, 30)
        )
        self.about_section_label = pygame_gui.elements.UILabel(
            relative_rect=about_section_rect,
            text="About",
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # About text
        about_text_rect = pygame.Rect(
            (panel_x + 20, about_section_rect.bottom + 10),
            (panel_width - 40, 120)
        )
        about_text = (
            "Double Pendulum Simulation\n"
            "Version 1.0\n\n"
            "Educational software for physics simulation.\n"
            "Designed for accessibility on low-end hardware."
        )
        self.about_text = pygame_gui.elements.UITextBox(
            html_text=about_text,
            relative_rect=about_text_rect,
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # Save button
        save_rect = pygame.Rect(
            (panel_x + 20, panel_y + panel_height - 60),
            ((panel_width - 60) // 2, 40)
        )
        self.save_button = pygame_gui.elements.UIButton(
            relative_rect=save_rect,
            text="Save Settings",
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
        # Back button
        back_rect = pygame.Rect(
            (save_rect.right + 20, panel_y + panel_height - 60),
            ((panel_width - 60) // 2, 40)
        )
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=back_rect,
            text="Back",
            manager=self.ui_manager,
            container=self.settings_panel
        )
        
    def update(self, deltaTime):
        """
        Update settings scene logic
        
        Args:
            deltaTime (float): Time elapsed since last update in seconds
        """
        # Update UI manager
        self.ui_manager.update(deltaTime)
        
    def render(self):
        """Render the settings scene to its surface"""
        # Fill background
        self.surface.fill(self.bg_color)
        
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
        
        # Handle UI element events
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.light_theme_button:
                    self._apply_theme("light")
                elif event.ui_element == self.dark_theme_button:
                    self._apply_theme("dark")
                elif event.ui_element == self.wire_checkbox:
                    self._toggle_wire_visibility()
                elif event.ui_element == self.save_button:
                    self.saveSettings()
                elif event.ui_element == self.back_button:
                    self._return_to_menu()
            
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.gravity_slider:
                    self._update_gravity(event.value)
                elif event.ui_element == self.fps_slider:
                    self._update_fps(int(event.value))
                elif event.ui_element == self.path_slider:
                    self._update_path_duration(event.value)
    
    def _apply_theme(self, theme_name):
        """
        Apply a theme to the application
        
        Args:
            theme_name (str): Name of the theme to apply (light/dark)
        """
        # Apply theme via config manager
        theme_colors = self.config_manager.applyTheme(theme_name)
        
        # Update local colors
        self.bg_color = theme_colors["background"]
        self.text_color = theme_colors["text"]
        
        # Recreate UI elements to apply theme (in a real app, would use theme files)
        self.ui_manager.clear_and_reset()
        self._create_ui_elements()
    
    def _toggle_wire_visibility(self):
        """Toggle the wire visibility setting"""
        current = self.config_manager.getSetting("show_wire")
        new_value = not current
        self.config_manager.setSetting("show_wire", new_value)
        
        # Update checkbox text
        self.wire_checkbox.set_text("✓" if new_value else " ")
    
    def _update_gravity(self, value):
        """
        Update the default gravity setting
        
        Args:
            value (float): New gravity value
        """
        self.config_manager.setSetting("gravity", value)
        self.gravity_label.set_text(f"Gravity: {value:.1f} m/s²")
    
    def _update_fps(self, value):
        """
        Update the FPS limit setting
        
        Args:
            value (int): New FPS limit
        """
        self.config_manager.setSetting("fps_limit", value)
        self.fps_label.set_text(f"FPS Limit: {value}")
    
    def _update_path_duration(self, value):
        """
        Update the path duration setting
        
        Args:
            value (float): New path duration in seconds
        """
        self.config_manager.setSetting("path_duration", value)
        self.path_label.set_text(f"Path Duration: {value:.1f}s")
    
    def saveSettings(self):
        """Save settings to configuration file"""
        success = self.config_manager.saveConfiguration()
        
        # In a real app, would show a success/failure message
        print(f"Settings saved: {success}")
    
    def loadSettings(self):
        """Load settings from configuration file"""
        self.config_manager.loadConfiguration()
        
        # Recreate UI elements to reflect loaded settings
        self.ui_manager.clear_and_reset()
        self._create_ui_elements()
    
    def _return_to_menu(self):
        """Return to the main menu"""
        # Save settings before leaving
        self.saveSettings()
        
        # Navigate back to home using direct app reference
        if self.app and hasattr(self.app, "sceneManager"):
            self.app.sceneManager.changeScene("home")
    
    def cleanup(self):
        """Clean up settings scene resources"""
        # Release UI manager resources
        self.ui_manager.clear_and_reset()