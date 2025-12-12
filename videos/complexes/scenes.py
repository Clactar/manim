from manim import *
from paramat_manim.creatures import EulerCreature, Blink, Look_Mobject, Reset_Look, Think, Angry, Happy


class SquareToCircle(Scene):
    def construct(self):
        square = Square()
        circle = Circle()

        square.set_fill(BLUE, opacity=0.5)
        circle.set_fill(GREEN, opacity=0.5)

        self.play(Create(square))
        self.play(Transform(square, circle))
        self.play(FadeOut(square))


class EulerCreatureDemo(Scene):
    def construct(self):
        e = EulerCreature().scale(0.6).to_corner(DL)
        target = Dot().to_corner(UR)

        self.play(FadeIn(e))
        self.play(Blink(e))
        self.play(FadeIn(target), Look_Mobject(e, target))

        bubble = e.right_speech_bubble(Text("Salut !").scale(0.8))
        self.play(FadeIn(bubble))
        self.play(Think(e))
        self.wait(0.5)
        self.play(Angry(e))
        self.wait(0.5)
        self.play(Happy(e), Reset_Look(e))
        self.play(FadeOut(bubble), FadeOut(target), FadeOut(e))


class EulerCreatureStatic(Scene):
    """Static scene for PNG export to check rendering."""
    def construct(self):
        e = EulerCreature().scale(0.6).to_corner(DL)
        bubble = e.right_speech_bubble(Text("Salut !").scale(0.8))
        self.add(e, bubble)


