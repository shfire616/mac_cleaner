import os.path

# Basics
app_name = "MacCleaner"
format = "UDZO" # Compressed
compression_level = 9
volume_name = "MacCleaner"

# Layout
window_rect = ((600, 600), (450, 300)) # Position, Size
background = None # Or path to image
icon_size = 100
text_size = 14

# Icon Locations
files = [ "dist/MacCleaner.app" ]
symlinks = { "Applications": "/Applications" }

icon_locations = {
    "MacCleaner.app": (120, 150),
    "Applications": (330, 150)
}
