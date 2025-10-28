"""
Icon Service - Creates system tray icon
Follows Single Responsibility Principle (SRP)
"""
from PIL import Image, ImageDraw


class IconService:
    """Service to create system tray icons."""
    
    @staticmethod
    def create_network_icon(size=64, color='green'):
        """
        Create a network/wifi style icon.
        
        Args:
            size: Icon size in pixels
            color: Icon color ('green', 'yellow', 'red', 'gray')
            
        Returns:
            PIL.Image: The generated icon
        """
        # Create a new image with transparency
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        
        # Color mapping
        colors = {
            'green': (0, 200, 0, 255),
            'yellow': (255, 200, 0, 255),
            'red': (220, 0, 0, 255),
            'gray': (128, 128, 128, 255)
        }
        
        fill_color = colors.get(color, colors['green'])
        
        # Draw wifi-style arcs (network signal icon)
        center_x = size // 2
        center_y = size // 2 + 5
        
        # Draw three signal arcs
        for i in range(3):
            radius = (i + 1) * (size // 8)
            thickness = max(2, size // 20)
            
            # Arc from 200 to 340 degrees (bottom arc)
            draw.arc(
                [center_x - radius, center_y - radius, 
                 center_x + radius, center_y + radius],
                start=200, end=340,
                fill=fill_color,
                width=thickness
            )
        
        # Draw center dot
        dot_radius = size // 12
        draw.ellipse(
            [center_x - dot_radius, center_y - dot_radius,
             center_x + dot_radius, center_y + dot_radius],
            fill=fill_color
        )
        
        return image
    
    @staticmethod
    def get_status_color(latency, threshold=1000):
        """
        Determine icon color based on network status.
        
        Args:
            latency: Current latency in ms (None if no response)
            threshold: Latency threshold for yellow/red
            
        Returns:
            str: Color name ('green', 'yellow', 'red', 'gray')
        """
        if latency is None:
            return 'red'
        elif latency > threshold:
            return 'yellow'
        else:
            return 'green'
