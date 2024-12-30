import tkinter as tk
from PIL import Image, ImageTk
import os

def is_nearly_black(pixel, threshold):
    """Check if a pixel is nearly black."""
    return pixel[0] < threshold and pixel[1] < threshold and pixel[2] < threshold

def load_frames(folder_path, output_folder, size=(800, 600), threshold=30, filename_prefix="AnimateEllipsesText_"):
    """Load all frames from the given folder, resize them, and save the processed images."""
    frame_files = sorted(
        [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(".png")]
    )
    frames = []
    for i, f in enumerate(frame_files):
        output_file = os.path.join(output_folder, f"{filename_prefix}{i:04d}.png")
        if os.path.exists(output_file):
            # Load the processed image if it exists
            img = Image.open(output_file).convert("RGBA")
        else:
            # Process the original image
            img = Image.open(f).convert("RGBA")  # Ensure image has an alpha channel
            img = img.resize(size)
            datas = img.getdata()

            # Remove black background
            new_data = []
            for item in datas:
                # Change all nearly black pixels to transparent
                if is_nearly_black(item, threshold):
                    new_data.append((255, 255, 255, 0))
                else:
                    new_data.append(item)
            img.putdata(new_data)
            
            # Save the processed image to the output folder
            img.save(output_file)

        frames.append(ImageTk.PhotoImage(img))
    return frames

def animate_frames(canvas, image_container, frames, delay):
    """Animate the frames on the canvas in a loop."""
    def update(index):
        if index < len(frames):
            # Update the image on the canvas
            canvas.itemconfig(image_container, image=frames[index])
            # Schedule the next frame
            root.after(delay, update, index + 1)
        else:
            # Restart from the first frame
            update(0)

    # Start the animation
    update(0)

# Tkinter setup
root = tk.Tk()
root.overrideredirect(True)  # Remove window decorations
root.geometry("800x600")  # Set window size
root.attributes('-transparentcolor', 'black')  # Set black as the transparent color

# Transparent canvas
canvas_width, canvas_height = 800, 600
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='black', highlightthickness=0)
canvas.pack()

# Load frames generated by Manim
frames_folder = "./processed_frames"  # Update to the correct path
output_folder = "./processed_frames"  # Update to the correct path
os.makedirs(output_folder, exist_ok=True)
filename_prefix = "AnimateEllipsesText_"  # Define the filename prefix
frames = load_frames(frames_folder, output_folder, size=(canvas_width, canvas_height), filename_prefix=filename_prefix)

# Add the first frame to the canvas
image_container = canvas.create_image(0, 0, anchor=tk.NW, image=frames[0])

# Animate the frames in a loop
frame_delay = 100  # Adjust the delay (in ms) for animation speed
animate_frames(canvas, image_container, frames, frame_delay)

# Make the window draggable
def move_window(event):
    root.geometry(f"+{event.x_root}+{event.y_root}")

canvas.bind("<B1-Motion>", move_window)

# Run the Tkinter event loop
root.mainloop()