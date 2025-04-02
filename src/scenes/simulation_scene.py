"""
SimulationScene - Main simulation scene for the Double Pendulum application
"""
import pygame
import pygame_gui
import math
import numpy as np
from src.scenes.scene import Scene
from src.physics.physics_engine import PhysicsEngine
from src.physics.pendulum_system import PendulumSystem
from src.physics.pendulum_params import PendulumParams

class SimulationScene(Scene):
    """
    The main simulation scene where users can interact with the double pendulum
    simulation. Includes controls for adjusting parameters, starting/stopping the
    simulation, and adding multiple pendulums.
    """
    
    def initialize(self, surface, config_manager, app_reference=None):
        """
        Initialize the simulation scene
        
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
        self.grid_color = theme_colors["grid"]
        
        # Initialize fonts
        self.title_font = pygame.font.SysFont('Arial', 36)
        self.normal_font = pygame.font.SysFont('Arial', 16)
        
        # Create physics engine
        self.physics_engine = PhysicsEngine()
        self.physics_engine.initialize(
            defaultGravity=self.config_manager.getSetting("gravity")
        )
        
        # Create pendulum system
        self.pendulum_system = PendulumSystem()
        self.pendulum_system.initialize()
        
        # Simulation state
        self.isRunning = False
        self.simulationSpeed = self.config_manager.getSetting("simulation_speed")
        self.simulation_time = 0.0
        
        # Control variables
        self.dragging = False  # Whether user is dragging a pendulum
        self.show_grid = True
        
        # Create UI elements
        self._create_ui_elements()
        
        # Create initial pendulums
        self._create_default_pendulum()
        
    def _create_default_pendulum(self):
        """Create a default pendulum for the simulation"""
        # Create default parameters for a simple pendulum
        params = PendulumParams()
        params.offsetX = self.width // 2
        params.offsetY = self.height // 3
        params.length1 = 120
        params.length2 = 120
        params.mass1 = 10
        params.mass2 = 10
        params.angle1 = math.pi / 4  # 45 degrees from vertical
        params.angle2 = math.pi / 2
        params.velocity1 = 0
        params.velocity2 = 0
        params.pathColor = pygame.Color(50, 100, 200)
        params.pathDuration = self.config_manager.getSetting("path_duration")
        params.showWire = self.config_manager.getSetting("show_wire")
        
        # Create the pendulum
        self.pendulum_system.createPendulum(params)
        
    def _create_ui_elements(self):
        """Create all UI elements for the simulation scene"""
        # Calculate control panel dimensions
        panel_width = 250
        panel_height = self.height
        panel_x = self.width - panel_width
        
        # Create background panel for controls
        self.control_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect(
                (panel_x, 0),
                (panel_width, panel_height)
            ),
            manager=self.ui_manager
        )
        
        # Simulation controls section
        title_rect = pygame.Rect(
            (panel_x + 10, 10),
            (panel_width - 20, 30)
        )
        self.title_label = pygame_gui.elements.UILabel(
            relative_rect=title_rect,
            text="Simulation Controls",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Start/Stop button
        button_rect = pygame.Rect(
            (panel_x + 10, title_rect.bottom + 10),
            (panel_width - 20, 40)
        )
        self.toggle_button = pygame_gui.elements.UIButton(
            relative_rect=button_rect,
            text="Start Simulation",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Reset button
        reset_rect = pygame.Rect(
            (panel_x + 10, button_rect.bottom + 10),
            (panel_width - 20, 40)
        )
        self.reset_button = pygame_gui.elements.UIButton(
            relative_rect=reset_rect,
            text="Reset Simulation",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Speed slider section
        speed_label_rect = pygame.Rect(
            (panel_x + 10, reset_rect.bottom + 20),
            (panel_width - 20, 20)
        )
        self.speed_label = pygame_gui.elements.UILabel(
            relative_rect=speed_label_rect,
            text=f"Simulation Speed: {self.simulationSpeed:.1f}x",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        speed_slider_rect = pygame.Rect(
            (panel_x + 10, speed_label_rect.bottom + 5),
            (panel_width - 20, 20)
        )
        self.speed_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=speed_slider_rect,
            start_value=self.simulationSpeed,
            value_range=(0.1, 3.0),
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Gravity slider section
        gravity_label_rect = pygame.Rect(
            (panel_x + 10, speed_slider_rect.bottom + 20),
            (panel_width - 20, 20)
        )
        self.gravity_label = pygame_gui.elements.UILabel(
            relative_rect=gravity_label_rect,
            text=f"Gravity: {self.physics_engine.gravity:.1f} m/s²",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        gravity_slider_rect = pygame.Rect(
            (panel_x + 10, gravity_label_rect.bottom + 5),
            (panel_width - 20, 20)
        )
        self.gravity_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=gravity_slider_rect,
            start_value=self.physics_engine.gravity,
            value_range=(1.0, 20.0),
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Pendulum settings section
        pendulum_label_rect = pygame.Rect(
            (panel_x + 10, gravity_slider_rect.bottom + 20),
            (panel_width - 20, 30)
        )
        self.pendulum_label = pygame_gui.elements.UILabel(
            relative_rect=pendulum_label_rect,
            text="Pendulum Parameters",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Add pendulum button
        add_pendulum_rect = pygame.Rect(
            (panel_x + 10, pendulum_label_rect.bottom + 10),
            (panel_width - 20, 30)
        )
        self.add_pendulum_button = pygame_gui.elements.UIButton(
            relative_rect=add_pendulum_rect,
            text="Add Pendulum",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Remove pendulum button
        remove_pendulum_rect = pygame.Rect(
            (panel_x + 10, add_pendulum_rect.bottom + 5),
            (panel_width - 20, 30)
        )
        self.remove_pendulum_button = pygame_gui.elements.UIButton(
            relative_rect=remove_pendulum_rect,
            text="Remove Selected Pendulum",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Toggle wire visibility
        toggle_wire_rect = pygame.Rect(
            (panel_x + 10, remove_pendulum_rect.bottom + 10),
            (panel_width - 20, 30)
        )
        self.toggle_wire_button = pygame_gui.elements.UIButton(
            relative_rect=toggle_wire_rect,
            text="Toggle Wire Visibility",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Path duration slider
        path_label_rect = pygame.Rect(
            (panel_x + 10, toggle_wire_rect.bottom + 20),
            (panel_width - 20, 20)
        )
        self.path_label = pygame_gui.elements.UILabel(
            relative_rect=path_label_rect,
            text=f"Path Duration: {self.config_manager.getSetting('path_duration'):.1f}s",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        path_slider_rect = pygame.Rect(
            (panel_x + 10, path_label_rect.bottom + 5),
            (panel_width - 20, 20)
        )
        self.path_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=path_slider_rect,
            start_value=self.config_manager.getSetting("path_duration"),
            value_range=(0.5, 10.0),
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Path color selection
        path_color_label_rect = pygame.Rect(
            (panel_x + 10, path_slider_rect.bottom + 20),
            (panel_width - 20, 20)
        )
        self.path_color_label = pygame_gui.elements.UILabel(
            relative_rect=path_color_label_rect,
            text="Path Color:",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Create color buttons
        color_button_width = (panel_width - 40) // 3
        color_button_height = 30
        color_y = path_color_label_rect.bottom + 5
        
        # Blue color button
        self.blue_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (panel_x + 10, color_y),
                (color_button_width, color_button_height)
            ),
            text="Blue",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Red color button
        self.red_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (panel_x + 20 + color_button_width, color_y),
                (color_button_width, color_button_height)
            ),
            text="Red",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Green color button
        self.green_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (panel_x + 30 + 2 * color_button_width, color_y),
                (color_button_width, color_button_height)
            ),
            text="Green",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
        # Back button
        back_y = self.height - 50
        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect(
                (panel_x + 10, back_y),
                (panel_width - 20, 40)
            ),
            text="Back to Menu",
            manager=self.ui_manager,
            container=self.control_panel
        )
        
    def update(self, deltaTime):
        """
        Update simulation scene logic
        
        Args:
            deltaTime (float): Time elapsed since last update in seconds
        """
        # Update simulation if running
        if self.isRunning:
            # Scale delta time by simulation speed
            scaled_dt = deltaTime * self.simulationSpeed
            
            # Update physics engine
            self.physics_engine.update(scaled_dt)
            
            # Update pendulum system
            self.pendulum_system.update(
                scaled_dt, 
                self.physics_engine.gravity
            )
            
            # Increment simulation time
            self.simulation_time += scaled_dt
        
        # Update UI manager
        self.ui_manager.update(deltaTime)
        
    def render(self):
        """Render the simulation scene to its surface"""
        # Fill background
        self.surface.fill(self.bg_color)
        
        # Draw grid if enabled
        if self.show_grid:
            self._draw_grid()
        
        # Draw simulation area boundary
        pygame.draw.rect(
            self.surface,
            (150, 150, 150),
            pygame.Rect(0, 0, self.width - 250, self.height),
            1
        )
        
        # Render pendulum system
        self.pendulum_system.render(self.surface)
        
        # Draw UI elements
        self.ui_manager.draw_ui(self.surface)
        
    def _draw_grid(self):
        """Draw a reference grid in the simulation area"""
        # Calculate grid spacing
        grid_spacing = 50
        
        # Calculate area to draw grid (exclude control panel)
        grid_width = self.width - 250
        
        # Draw horizontal lines
        for y in range(0, self.height, grid_spacing):
            pygame.draw.line(
                self.surface,
                self.grid_color,
                (0, y),
                (grid_width, y),
                1
            )
        
        # Draw vertical lines
        for x in range(0, grid_width, grid_spacing):
            pygame.draw.line(
                self.surface,
                self.grid_color,
                (x, 0),
                (x, self.height),
                1
            )
        
    def handleEvent(self, event):
        """
        Handle a pygame event
        
        Args:
            event (pygame.event.Event): The event to handle
        """
        # Process event through UI manager
        self.ui_manager.process_events(event)
        
        # Handle mouse events for pendulum interaction
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left button
                # Check if click is in simulation area (not on control panel)
                if event.pos[0] < (self.width - 250):
                    # Try to start dragging a pendulum
                    self.dragging = self.pendulum_system.startDrag(event.pos)
        
        elif event.type == pygame.MOUSEMOTION:
            # Update drag operation if in progress
            if self.dragging:
                self.pendulum_system.updateDrag(event.pos)
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1 and self.dragging:  # Left button
                self.pendulum_system.endDrag()
                self.dragging = False
        
        # Handle UI element events
        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == self.toggle_button:
                    self.toggleSimulation()
                elif event.ui_element == self.reset_button:
                    self.resetSimulation()
                elif event.ui_element == self.add_pendulum_button:
                    self._add_new_pendulum()
                elif event.ui_element == self.remove_pendulum_button:
                    self._remove_selected_pendulum()
                elif event.ui_element == self.toggle_wire_button:
                    self._toggle_wire_visibility()
                elif event.ui_element == self.back_button:
                    self._return_to_menu()
                elif event.ui_element == self.blue_button:
                    self._set_path_color(50, 100, 200)  # Blue
                elif event.ui_element == self.red_button:
                    self._set_path_color(200, 50, 50)  # Red
                elif event.ui_element == self.green_button:
                    self._set_path_color(50, 180, 50)  # Green
            
            elif event.user_type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                if event.ui_element == self.speed_slider:
                    self.adjustSpeed(event.value)
                elif event.ui_element == self.gravity_slider:
                    self._adjust_gravity(event.value)
                elif event.ui_element == self.path_slider:
                    self._adjust_path_duration(event.value)
    
    def toggleSimulation(self):
        """Toggle the simulation between running and paused states"""
        self.isRunning = not self.isRunning
        
        # Update button text
        if self.isRunning:
            self.toggle_button.set_text("Pause Simulation")
        else:
            self.toggle_button.set_text("Resume Simulation")
    
    def resetSimulation(self):
        """Reset all pendulums to their initial states"""
        self.pendulum_system.resetAll()
        self.simulation_time = 0.0
        
        # If simulation was running, keep it running
        if not self.isRunning:
            # Otherwise update the button text
            self.toggle_button.set_text("Start Simulation")
    
    def adjustSpeed(self, amount):
        """
        Adjust the simulation speed
        
        Args:
            amount (float): New simulation speed
        """
        self.simulationSpeed = amount
        self.config_manager.setSetting("simulation_speed", amount)
        
        # Update label
        self.speed_label.set_text(f"Simulation Speed: {self.simulationSpeed:.1f}x")
    
    def _adjust_gravity(self, value):
        """
        Adjust the gravity value
        
        Args:
            value (float): New gravity value
        """
        self.physics_engine.setGravity(value)
        self.config_manager.setSetting("gravity", value)
        
        # Update label
        self.gravity_label.set_text(f"Gravity: {value:.1f} m/s²")
    
    def _adjust_path_duration(self, value):
        """
        Adjust the path duration
        
        Args:
            value (float): New path duration in seconds
        """
        self.config_manager.setSetting("path_duration", value)
        
        # Update label
        self.path_label.set_text(f"Path Duration: {value:.1f}s")
        
        # Update path tracers for all pendulums
        for pendulum in self.pendulum_system.pendulums:
            if pendulum.pathTracer:
                pendulum.pathTracer.setDuration(value)
    
    def _add_new_pendulum(self):
        """Add a new pendulum to the simulation"""
        # Create parameters for a new pendulum with random angles
        params = PendulumParams()
        params.offsetX = self.width // 2
        params.offsetY = self.height // 3
        params.length1 = 120
        params.length2 = 120
        params.mass1 = 10
        params.mass2 = 10
        params.angle1 = math.pi/2 * (0.5 + 0.5 * np.random.random())
        params.angle2 = math.pi/2 * (0.5 + 0.5 * np.random.random())
        params.velocity1 = 0
        params.velocity2 = 0
        
        # Get color from configuration
        path_color = self.config_manager.getSetting("path_color")
        params.pathColor = pygame.Color(path_color[0], path_color[1], path_color[2])
        
        params.pathDuration = self.config_manager.getSetting("path_duration")
        params.showWire = self.config_manager.getSetting("show_wire")
        
        # Create the pendulum
        self.pendulum_system.createPendulum(params)
    
    def _remove_selected_pendulum(self):
        """Remove the currently selected pendulum"""
        selected = self.pendulum_system.getSelectedPendulum()
        if selected and len(self.pendulum_system.pendulums) > 1:
            self.pendulum_system.removePendulum(selected.id)
    
    def _toggle_wire_visibility(self):
        """Toggle wire visibility for the selected pendulum"""
        selected = self.pendulum_system.getSelectedPendulum()
        if selected:
            selected.toggleWireVisibility()
            # Update configuration
            self.config_manager.setSetting("show_wire", selected.showWire)
    
    def _set_path_color(self, r, g, b):
        """
        Set the path color for the selected pendulum
        
        Args:
            r (int): Red component (0-255)
            g (int): Green component (0-255)
            b (int): Blue component (0-255)
        """
        selected = self.pendulum_system.getSelectedPendulum()
        if selected and selected.pathTracer:
            selected.pathTracer.setColor(r, g, b)
            
            # Update configuration
            self.config_manager.setSetting("path_color", [r, g, b])
    
    def _return_to_menu(self):
        """Return to the main menu"""
        if self.app and hasattr(self.app, "sceneManager"):
            self.app.sceneManager.changeScene("home")
    
    def cleanup(self):
        """Clean up simulation scene resources"""
        # Release UI manager resources
        self.ui_manager.clear_and_reset()