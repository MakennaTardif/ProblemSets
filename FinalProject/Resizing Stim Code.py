# ONE-TIME RESIZE ORIGINAL STIM FILES

# The original images were very large (i.e., 2444 × 1718 pixels). 
# PsychoPy loads full-resolution textures into RAM, even if they are displayed smaller. 
# Because the experiment will display 6 faces at once, using full-sized images would cause slowdowns, frame drops, and high memory usage.
# To avoid this, all original stimuli are resized once at the beginning of the script. 
# The resized copies are saved to a new folder ("stimuli_small") and used for the rest of the experiment.
# This block only needs to run the first time. 
# Afterwards, the folder already exists and contains optimized images.

from PIL import Image   # https://pytutorial.com/python-pil-image-handling-guide/  (i.e., image processing library used for resizing stimulus files)
import os               # https://docs.python.org/3/library/os.html (i.e., tools for listing files, creating directories, and building file paths)

original_folder = "stimuli"          # Folder containing the original large images
small_folder    = "stimuli_small"    # Folder that will store the resized images
os.makedirs(small_folder, exist_ok=True)

TARGET_SIZE = (240, 180)  # Width × height in pixels
                          # This is sufficient for displaying 6 faces on fullscreen.

count = 0  # Counter for how many images are processed 

# Loop through all files in the original folder
for fname in os.listdir(original_folder):

    # Resize .jpg images
    if not fname.lower().endswith(".jpg"): # Only process .jpg files; ignore all other file types (there shouldn't be any others but this is just in case)
        continue

    # Building the full path to the current image file
    in_path = os.path.join(original_folder, fname)

    # Load the original large image using PIL
    img = Image.open(in_path)

    # Resizing the image to the target resolution using LANCZOS
    img_small = img.resize(TARGET_SIZE, Image.LANCZOS)  # This is a high-quality downsampling filter (https://www.geeksforgeeks.org/python/python-pil-image-resize-method/)

    # Save the resized version into the new folder
    out_path = os.path.join(small_folder, fname)  # Save the resized image into the new folder, preserving the original filename.
    img_small.save(out_path, optimize=True)   # optimize=True reduces file size further

    count += 1  # I wanted to track how many images we resized (i.e.., This should be 126 - 108 images + 18 foils)

print(f"Done resizing {count} JPGs into {small_folder}")  # Confirm in the console that all images have been resized and saved.
