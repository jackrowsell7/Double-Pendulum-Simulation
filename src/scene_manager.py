"""
SceneManager - Manages application scenes and transitions between them
"""

class SceneManager:
    """
    Manages different scenes in the application and handles transitions
    between them. Implements the State pattern for scene management.
    """
    
    def __init__(self):
        """Initialize the SceneManager with empty scenes dictionary"""
        self.currentScene = None
        self.scenes = {}
        
    def initialize(self):
        """Initialize the scene manager"""
        pass
        
    def changeScene(self, sceneName):
        """
        Change to a different scene
        
        Args:
            sceneName (str): The name of the scene to change to
        
        Returns:
            bool: True if scene change was successful, False otherwise
        """
        print(f"SceneManager.changeScene called with sceneName: {sceneName}")
        print(f"Available scenes: {list(self.scenes.keys())}")
        if sceneName not in self.scenes:
            print(f"Scene '{sceneName}' not found")
            return False
            
        # If we have a current scene, clean it up
        if self.currentScene:
            print(f"Cleaning up current scene")
            self.currentScene.cleanup()
            
        # Set the new scene
        print(f"Setting new scene to: {sceneName}")
        self.currentScene = self.scenes[sceneName]
        return True
        
    def getCurrentScene(self):
        """
        Get the current active scene
        
        Returns:
            Scene: The current scene object
        """
        return self.currentScene
        
    def registerScene(self, name, scene):
        """
        Register a scene with the manager
        
        Args:
            name (str): Name to register the scene under
            scene (Scene): The scene object to register
        """
        self.scenes[name] = scene