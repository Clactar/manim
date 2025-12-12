from manim import *


class SquareToCircle(Scene):
    def construct(self):
        square = Square()
        circle = Circle()

        square.set_fill(BLUE, opacity=0.5)
        circle.set_fill(GREEN, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


