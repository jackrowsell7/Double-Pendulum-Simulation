#!/usr/bin/env python3
"""
Double Pendulum Simulation - Main Entry Point
Educational application for simulating double pendulum physics
"""
import os
import sys
import pygame
import pygame_gui

from src.app import DoublePendulumApp

# Global app instance that will be accessible to all modules
app = None

def main():
    """Main entry point for the Double Pendulum Simulation application"""
    # Initialize the application
    global app
    app = DoublePendulumApp()
    app.initialize()
    
    # Run the application
    try:
        app.run()
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up resources
        app.exit()

if __name__ == "__main__":
    main()