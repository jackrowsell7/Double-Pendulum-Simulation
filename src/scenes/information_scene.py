"""
InformationScene - Educational information and instructions for the Double Pendulum Simulation
"""
import pygame
import pygame_gui
from src.scenes.scene import Scene

class InformationScene(Scene):
    """
    Information scene that provides educational content and instructions
    about double pendulums and how to use the simulation application.
    """
    
    def initialize(self, surface, config_manager, app_reference=None):
        """
        Initialize the information scene
        
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
        self.heading_font = pygame.font.SysFont('Arial', 24)
        self.normal_font = pygame.font.SysFont('Arial', 16)
        
        # Initialize information sections
        self.current_section = 0
        self.info_sections = [
            {
                "title": "About Double Pendulums",
                "content": """
                <b>Double Pendulum Physics</b><br><br>
                A double pendulum consists of one pendulum attached to the end of another. 
                This system is a classic example of a chaotic system in physics.<br><br>
                
                Key characteristics:<br>
                - Double pendulums exhibit chaotic motion under certain conditions<br>
                - Small changes in initial conditions lead to vastly different trajectories<br>
                - The motion equations include nonlinear terms that make analytical solutions difficult<br>
                - The system has two degrees of freedom and higher-order dynamics<br><br>
                
                Despite the simple construction, the double pendulum demonstrates the fascinating 
                complexity that can arise from relatively simple physical systems.
                """
            },
            {
                "title": "Using the Simulation",
                "content": """
                <b>How to Use the Simulation</b><br><br>
                
                <b>Basic Controls:</b><br>
                - Start/Pause: Control the simulation using the start/pause button<br>
                - Reset: Return pendulums to their initial positions<br>
                - Speed: Adjust simulation speed using the slider<br>
                - Gravity: Modify the gravitational constant<br><br>
                
                <b>Pendulum Interaction:</b><br>
                - Add pendulums to create multiple systems<br>
                - Click and drag a pendulum bob to position it manually<br>
                - Toggle wire visibility to focus on the pendulum path<br>
                - Change the path color and duration<br><br>
                
                Experiment with different initial angles and settings to observe 
                how chaotic behavior develops over time.
                """
            },
            {
                "title": "Educational Resources",
                "content": """
                <b>Learn More About Physics</b><br><br>
                
                <b>Further Reading:</b><br>
                - "Chaos: Making a New Science" by James Gleick<br>
                - "Nonlinear Dynamics and Chaos" by Steven Strogatz<br>
                - "The Feynman Lectures on Physics, Vol. I" by Richard Feynman<br><br>
                
                <b>Online Resources:</b><br>
                - Khan Academy: Pendulum Physics<br>
                - MIT OpenCourseWare: Classical Mechanics<br>
                - Physics Classroom: Oscillatory Motion<br><br>
                
                <b>Principles Demonstrated:</b><br>
                - Conservation of Energy<br>
                - Chaos Theory<br>
                - Nonlinear Dynamics<br>
                - Sensitivity to Initial Conditions (Butterfly Effect)<br>
                """
            }
        ]
        
        # Create UI elements
        self._create_ui_elements()
        
    def _create_ui_elements(self):
        """Create all UI elements for the information scene"""
        # Create panel for information
        panel_width = 800
        panel_height = 600
        panel_x = self.width // 2 - panel_width // 2
        panel_y = self.height // 2 - panel_height // 2
        
        self.info_panel = pygame_gui.elements.UIPanel(
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
            text="Information & Instructions",
            manager=self.ui_manager,
            container=self.info_panel
        )
        
        # Section navigation
        nav_width = 200
        
        # Create section buttons
        section_buttons_y = title_rect.bottom + 20
        self.section_buttons = []
        
        for i, section in enumerate(self.info_sections):
            button_rect = pygame.Rect(
                (panel_x + 20, section_buttons_y + i * 50),
                (nav_width, 40)
            )
            
            button = pygame_gui.elements.UIButton(
                relative_rect=button_rect,
                text=section["title"],
                manager=self.ui_manager,
                container=self.info_panel
            )
            
            self.section_buttons.append(button)
        
        # Section title
        section_title_rect = pygame.Rect(
            (panel_x + nav_width + 40, title_rect.bottom + 20),
            (panel_width - nav_width - 60, 40)
        )
        self.section_title = pygame_gui.elements.UILabel(
            relative_rect=section_title_rect,
            text=self.info_sections[self.current_section]["title"],
            manager=self.ui_manager,
            container=self.info_panel
        )
        
        # Section content
        content_rect = pygame.Rect(
            (panel_x + nav_width + 40, section_title_rect.bottom + 10),
            (panel_width - nav_width - 60, panel_height - section_title_rect.bottom - 80)
        )
        self.content_textbox = pygame_gui.elements.UITextBox(
            html_text=self.info_sections[self.current_section]["content"],
            relative_rect=content_rect,
            manager=self.ui_manager,
            container=self.info_panel
        )
        
        # Back button
        back_rect = pygame.Rect(
            (panel_x + panel_width - 120, panel_y + panel_height - 60),
            (100, 40)
        )
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=back_rect,
            text="Back",
            manager=self.ui_manager,
            container=self.info_panel
        )
        
    def update(self, deltaTime):
        """
        Update information scene logic
        
        Args:
            deltaTime (float): Time elapsed since last update in seconds
        """
        # Update UI manager
        self.ui_manager.update(deltaTime)
        
    def render(self):
        """Render the information scene to its surface"""
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
                if event.ui_element == self.back_button:
                    self._return_to_menu()
                else:
                    # Check if a section button was pressed
                    for i, button in enumerate(self.section_buttons):
                        if event.ui_element == button:
                            self.navigateSection(i)
                            break
    
    def navigateSection(self, sectionIndex):
        """
        Navigate to a specific information section
        
        Args:
            sectionIndex (int): Index of the section to navigate to
        """
        if 0 <= sectionIndex < len(self.info_sections):
            self.current_section = sectionIndex
            
            # Update section title and content
            self.section_title.set_text(self.info_sections[sectionIndex]["title"])
            self.content_textbox.set_text(self.info_sections[sectionIndex]["content"])
    
    def _return_to_menu(self):
        """Return to the main menu"""
        # Navigate back to home using direct app reference
        if self.app and hasattr(self.app, "sceneManager"):
            self.app.sceneManager.changeScene("home")
    
    def cleanup(self):
        """Clean up information scene resources"""
        # Release UI manager resources
        self.ui_manager.clear_and_reset()