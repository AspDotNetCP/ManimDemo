# Manim Demo with Tkinter Integration

This repository demonstrates how to create animations using Manim and integrate them into a Tkinter application. The animations are rendered using Manim, converted to a sequence of PNG images using `ffmpeg`, and then displayed in a Tkinter window.

## Prerequisites

- Python 3.x
- Manim
- Tkinter
- PIL (Pillow)
- ffmpeg

## Installation

1. Install Manim and other dependencies using Chocolatey and pip:

    ```sh
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

    choco install manimce
    choco install manim-latex
    choco install vscode
    pip install tkvideo
    pip install pillow
    ```

2. Install `ffmpeg`:

    ```sh
    choco install ffmpeg
    ```

## Usage

1. Create and render the Manim scene:

    ```sh
    manim -pql Example.py HelloWorldAndEllipse
    ```

    This will create a video file named `HelloWorldAndEllipse.mp4` in the [480p15](http://_vscodecontentref_/0) directory.

2. Convert the video to a sequence of PNG images using `ffmpeg`:

    ```sh
    ffmpeg -i media/videos/Example/480p15/HelloWorldAndEllipse.mp4 frames_folder/frame_%04d.png
    ```

3. Run the Tkinter application to display the animation:

    ```sh
    python main.py
    ```

## Files

- [Example.py](http://_vscodecontentref_/1): Contains the Manim scene definitions.
- [main.py](http://_vscodecontentref_/2): Contains the Tkinter application code to load and display the animation frames.
- [requirements.txt](http://_vscodecontentref_/3): Lists the dependencies and commands to set up the environment.

## [Example.py](http://_vscodecontentref_/4)

This file defines the Manim scenes. The `HelloWorldAndEllipse` scene combines the `HelloWorld` and `AnimatedSquareToCircle` animations, adds multiple ellipses, and animates them bouncing to the left top.

```python
from manim import *

class HelloWorldAndEllipse(Scene):
    def construct(self):
        # Create an ellipse
        ellipse = Ellipse(width=2, height=1)
        ellipse.set_fill(BLUE, opacity=0.5)

        # Create another ellipse
        ellipse2 = Ellipse(width=2, height=1)
        ellipse2.set_fill(RED, opacity=0.5)

        # Create a Text object
        hello_world = Text("Hello, World!")

        # Position the text at the center of the ellipse
        hello_world.move_to(ellipse.get_center())

        # Display the ellipse and text
        self.play(Create(ellipse), Write(hello_world))
        self.wait(1)

        # Transform the first ellipse into the second ellipse and move the text with it
        self.play(Transform(ellipse, ellipse2), ApplyMethod(hello_world.move_to, ellipse2.get_center()))
        self.wait(1)

        # Move the ellipse and text to the top left of the frame
        self.play(ellipse.animate.to_corner(UL), hello_world.animate.to_corner(UL))
        self.wait(1)

        # Create multiple ellipses
        ellipses = VGroup(*[Ellipse(width=2, height=1, color=YELLOW).shift(UP * i) for i in range(5)])

        # Display the ellipses
        self.play(Create(ellipses))
        self.wait(1)

        # Animate the ellipses bouncing to the left top
        for ellipse in ellipses:
            self.play(ellipse.animate.shift(LEFT * 2 + UP * 2), run_time=2, rate_func=there_and_back)
        self.wait(1)