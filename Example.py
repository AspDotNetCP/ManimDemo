from manim import *

# class TransparentCircleScene(Scene):
#     def construct(self):
#         # Set the background color to transparent
#         self.camera.background_color = None

#         # Create a red circle
#         circle = Circle()
        
#         # Animate the circle
#         self.play(Create(circle))  # Create the circle
#         self.play(circle.animate.shift(UP))  # Move the circle up
#         self.play(FadeOut(circle))  # Fade the circle out

from manim import *

class AnimatedSquareToCircle(Scene):
    def construct(self):
        # Create a square
        square = Square()
        square.set_fill(BLUE, opacity=0.5)

        # Create a circle
        circle = Circle()
        circle.set_fill(RED, opacity=0.5)

        # Create a Text object
        hello_world = Text("Hello, World!")

        # Position the text at the center of the square
        hello_world.move_to(square.get_center())

        # Display the square and text
        self.play(Create(square), Write(hello_world))
        self.wait(1)

        # Transform the square into a circle and move the text with it
        self.play(Transform(square, circle), ApplyMethod(hello_world.move_to, circle.get_center()))
        self.wait(1)

class HelloWorldAndSquareToCircle(Scene):
    def construct(self):
        # Create a square
        square = Square()
        square.set_fill(BLUE, opacity=0.5)

        # Create a circle
        circle = Circle()
        circle.set_fill(RED, opacity=0.5)

        # Create a Text object
        hello_world = Text("Hello, World!")

        # Position the text at the center of the square
        hello_world.move_to(square.get_center())

        # Display the square and text
        self.play(Create(square), Write(hello_world))
        self.wait(1)

        # Transform the square into a circle and move the text with it
        self.play(Transform(square, circle), ApplyMethod(hello_world.move_to, circle.get_center()))
        self.wait(1)

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

# class AnimatedSquareToCircle(Scene):
#     def construct(self):
#         circle = Circle()  # create a circle
#         square = Square()  # create a square

#         self.play(Create(square))  # show the square on screen
#         self.play(square.animate.rotate(PI / 4))  # rotate the square
#         self.play(Transform(square, circle))  # transform the square into a circle
#         self.play(
#             square.animate.set_fill(PINK, opacity=0.5)
#         )  # color the circle on screen