"""
EulerCreature: the animated "e" mascot for Paramat videos.
Ported faithfully from the original euler_creature.py.
"""
from __future__ import annotations

import shutil
from typing import Optional

import numpy as np
from numpy import maximum, minimum
from manim import (
    BLACK,
    BLUE,
    WHITE,
    LEFT,
    RIGHT,
    UL,
    UP,
    UR,
    PI,
    Arc,
    Circle,
    Dot,
    Ellipse,
    Line,
    MathTex,
    Tex,
    Text,
    VGroup,
    normalize,
)


def _has_latex() -> bool:
    return shutil.which("latex") is not None


class EulerCreature(VGroup):
    """
    Animated "e" creature with eyes, expressions, and speech bubbles.
    Matches the original euler_creature.py rendering as closely as possible.
    """

    def __init__(self, color: str = BLUE, **kwargs):
        super().__init__(**kwargs)
        self._color = color

        # -----------------------------------------------------------------
        # Body (MathTex for nice italic "e", fallback to italic serif Text)
        # -----------------------------------------------------------------
        if _has_latex():
            self.body = MathTex("e", color=color).scale(8.217)
        else:
            # Fallback: italic serif font that looks similar to LaTeX math "e"
            self.body = Text(
                "e",
                color=color,
                font="Times New Roman",
                slant="ITALIC",
            ).scale(8.217 * 0.75)

        # -----------------------------------------------------------------
        # Eyes (white sclera)
        # -----------------------------------------------------------------
        self.left_white = Dot(color=WHITE).scale(1.5).next_to(self.body, UP, buff=-0.02)
        self.right_white = Dot(color=WHITE).scale(1.5).next_to(self.left_white, RIGHT, buff=-0.001)

        # -----------------------------------------------------------------
        # Pupils (black dot + white glint)
        # -----------------------------------------------------------------
        self.left_black = Dot(color=BLACK).scale(0.75).move_to(self.left_white)
        self.left_black_white = Dot(color=WHITE).scale(0.2).next_to(self.left_black, UR, buff=-0.05)

        self.right_black = Dot(color=BLACK).scale(0.75).move_to(self.right_white)
        self.right_black_white = Dot(color=WHITE).scale(0.2).next_to(self.right_black, UR, buff=-0.05)

        # -----------------------------------------------------------------
        # Mouth (happy smile by default)
        # -----------------------------------------------------------------
        if _has_latex():
            self.mouth = Tex("(").rotate(PI / 2).next_to(self.body, buff=0).shift([-0.9, 0.5, 0])
        else:
            self.mouth = Text("(", font="Times New Roman").rotate(PI / 2).next_to(
                self.body, buff=0
            ).shift([-0.9, 0.5, 0])

        # -----------------------------------------------------------------
        # Add submobjects (same order as original for index compatibility)
        # -----------------------------------------------------------------
        self.add(
            self.body,              # 0
            self.left_white,        # 1
            self.right_white,       # 2
            self.left_black,        # 3
            self.left_black_white,  # 4
            self.right_black,       # 5
            self.right_black_white, # 6
            self.mouth,             # 7
        )

        # Convenience groups
        self.pupils = VGroup(self.left_black, self.left_black_white,
                             self.right_black, self.right_black_white)
        self.eyes = VGroup(self.pupils, self.left_white, self.right_white)

    # =====================================================================
    # Accessors
    # =====================================================================

    def get_body(self):
        return self.body

    def get_eyes(self) -> VGroup:
        return VGroup(
            self.left_white, self.right_white,
            self.left_black, self.left_black_white,
            self.right_black, self.right_black_white,
        )

    def get_pupils(self) -> VGroup:
        return VGroup(
            self.left_black, self.left_black_white,
            self.right_black, self.right_black_white,
        )

    # =====================================================================
    # Eye animations
    # =====================================================================

    def blink(self, **kwargs) -> "EulerCreature":
        """Flatten eyes vertically to simulate a blink."""
        eyes = self.get_eyes()
        bottom_y = eyes.get_bottom()[1]
        for submob in eyes:
            submob.apply_function(lambda p: [p[0], bottom_y, p[2]])
        return self

    def look_in_direction(self, vect) -> "EulerCreature":
        """Move pupils towards target point, clamped inside sclera."""
        coeff = min(self.left_white.get_width(), self.left_black.get_width()) / 2
        eyes_center = self.get_eyes().get_center()
        direction = normalize(np.array(vect) - eyes_center) * coeff

        left_center = self.left_white.get_center()
        right_center = self.right_white.get_center()

        VGroup(self.left_black, self.left_black_white).move_to(left_center + direction)
        VGroup(self.right_black, self.right_black_white).move_to(right_center + direction)
        return self

    def look_at(self, mob) -> "EulerCreature":
        """Look at another mobject."""
        return self.look_in_direction(mob.get_center())

    def look_reset(self) -> "EulerCreature":
        """Reset pupils to center of eyes."""
        scale_factor = maximum(self.right_white.get_width(), self.right_white.get_height()) / Dot().get_width()

        new_left_eye = Dot(color=WHITE).scale(scale_factor).next_to(self.body, UP, buff=-0.02 * scale_factor)
        new_right_eye = Dot(color=WHITE).scale(scale_factor).next_to(new_left_eye, RIGHT, buff=-0.001 * scale_factor)

        d = np.abs(new_right_eye.get_center() - new_left_eye.get_center())
        right_center = new_right_eye.get_center()
        left_center = right_center + d * LEFT

        VGroup(self.left_black, self.left_black_white).move_to(left_center)
        VGroup(self.right_black, self.right_black_white).move_to(right_center)
        return self

    # =====================================================================
    # Expressions
    # =====================================================================

    def _new_mouth(self, char: str, rotation: float):
        """Create a new mouth mobject matching the current mouth size."""
        if _has_latex():
            m = Tex(char).rotate(rotation).move_to(self.mouth)
        else:
            m = Text(char, font="Times New Roman").rotate(rotation).move_to(self.mouth)
        m.set(width=self.mouth.get_width())
        return m

    def happy(self) -> "EulerCreature":
        """Set happy expression (smile)."""
        scale_factor = maximum(self.right_white.get_width(), self.right_white.get_height()) / Dot().get_width()

        new_left_eye = Dot(color=WHITE).scale(scale_factor).next_to(self.body, UP, buff=-0.02 * scale_factor)
        new_right_eye = Dot(color=WHITE).scale(scale_factor).next_to(new_left_eye, RIGHT, buff=-0.001 * scale_factor)

        new_mouth = self._new_mouth("(", PI / 2)

        self.left_white.become(new_left_eye)
        self.right_white.become(new_right_eye)
        self.mouth.become(new_mouth)
        return self

    def happy_reset(self) -> "EulerCreature":
        """Set happy expression and reset pupils to center."""
        scale_factor = maximum(self.right_white.get_width(), self.right_white.get_height()) / Dot().get_width()

        new_left_eye = Dot(color=WHITE).scale(scale_factor).next_to(self.body, UP, buff=-0.02 * scale_factor)
        new_right_eye = Dot(color=WHITE).scale(scale_factor).next_to(new_left_eye, RIGHT, buff=-0.001 * scale_factor)

        new_mouth = self._new_mouth("(", PI / 2)

        d = np.abs(new_right_eye.get_center() - new_left_eye.get_center())
        right_center = new_right_eye.get_center()
        left_center = right_center + d * LEFT

        self.left_white.become(new_left_eye)
        self.right_white.become(new_right_eye)
        self.mouth.become(new_mouth)

        VGroup(self.left_black, self.left_black_white).move_to(left_center)
        VGroup(self.right_black, self.right_black_white).move_to(right_center)
        return self

    def angry(self) -> "EulerCreature":
        """Set angry expression (frown + furrowed brows)."""
        radius = self.right_white.get_height()
        center_left = self.left_white.get_center()
        center_right = self.right_white.get_center()
        scale_factor = maximum(self.right_white.get_width(), self.right_white.get_height()) / Dot().get_width()

        new_mouth = self._new_mouth("(", -PI / 2)

        new_left_eye = Dot(color=WHITE).scale(scale_factor).move_to(self.left_white)
        new_right_eye = Dot(color=WHITE).scale(scale_factor).move_to(self.right_white)
        self.left_white.become(new_left_eye)
        self.right_white.become(new_right_eye)

        def angry_right(m):
            if m[0] <= center_right[0] and m[1] >= center_right[1]:
                m[1] = minimum(m[1], m[0] + 0.5 * radius + center_right[1] - center_right[0])
            return m

        def angry_left(m):
            if m[0] >= center_left[0] and m[1] >= center_left[1]:
                m[1] = minimum(m[1], -m[0] + 0.5 * radius + center_left[1] + center_left[0])
            return m

        self.left_white.apply_function(angry_left)
        self.right_white.apply_function(angry_right)
        self.mouth.become(new_mouth)
        return self

    def thinking(self) -> "EulerCreature":
        """Set thinking expression (squinted eyes + tilted mouth)."""
        radius = self.left_white.get_height()
        scale_factor = maximum(self.right_white.get_width(), self.right_white.get_height()) / Dot().get_width()

        new_left_eye = Dot(color=WHITE).scale(scale_factor).move_to(self.left_white)
        new_left_eye.stretch_to_fit_width(self.left_white.get_width() / 1.2)
        new_right_eye = Dot(color=WHITE).scale(scale_factor).move_to(self.right_white)
        new_right_eye.stretch_to_fit_width(self.left_white.get_width() / 1.2)

        self.left_white.become(new_left_eye)
        self.right_white.become(new_right_eye)

        center_left = self.left_white.get_center()

        new_mouth = self._new_mouth("/", -PI / 3)

        def think(m):
            m[1] = minimum(m[1], center_left[1] + radius / 3.5)
            return m

        self.mouth.become(new_mouth)
        self.left_white.apply_function(think)
        return self

    # =====================================================================
    # Speech / Thought Bubbles
    # =====================================================================

    def _bubble_dimensions(self, content):
        if content.get_width() > content.get_height():
            bubble_width = 1.2 * content.get_width()
            bubble_height = 1.2 * max(content.get_width() / 2, content.get_height())
        else:
            bubble_height = 1.2 * content.get_height()
            bubble_width = 1.2 * max(content.get_height() / 2, content.get_width())
        return bubble_width, bubble_height

    def _tail_start_factor(self) -> float:
        if _has_latex():
            ref_height = MathTex("e").scale(8.5).get_height()
        else:
            ref_height = self.body.get_height()
        return self.get_height() / ref_height

    def right_speech_bubble(self, content) -> VGroup:
        a = 1.5 * self.get_height() / max(content.get_height(), content.get_width())
        content.scale(a)
        bubble_width, bubble_height = self._bubble_dimensions(content)
        content.next_to(self, UR, buff=0.5)

        ellipse = Arc(start_angle=-4 * PI / 6, angle=15 * PI / 8)
        ellipse.stretch_to_fit_height(bubble_height)
        ellipse.stretch_to_fit_width(bubble_width)
        ellipse.move_to(content).scale(1.2)

        mob_start = self.get_center() + UR * 0.6 * self._tail_start_factor()
        left_line = Line(mob_start, ellipse.get_start())
        right_line = Line(mob_start, ellipse.get_end())
        cont_bubble = VGroup(ellipse, left_line, right_line).set_stroke(width=1)
        return VGroup(cont_bubble, content)

    def left_speech_bubble(self, content) -> VGroup:
        a = 1.5 * self.get_height() / max(content.get_height(), content.get_width())
        content.scale(a)
        bubble_width, bubble_height = self._bubble_dimensions(content)
        content.next_to(self, UL, buff=0.5)

        ellipse = Arc(start_angle=-PI / 6, angle=15 * PI / 8)
        ellipse.stretch_to_fit_height(bubble_height)
        ellipse.stretch_to_fit_width(bubble_width)
        ellipse.move_to(content).scale(1.2)

        mob_start = self.get_center() + UL * 0.6 * self._tail_start_factor()
        left_line = Line(mob_start, ellipse.get_start())
        right_line = Line(mob_start, ellipse.get_end())
        cont_bubble = VGroup(ellipse, left_line, right_line).set_stroke(width=1)
        return VGroup(cont_bubble, content)

    def right_thought_bubble(self, content) -> VGroup:
        a = 2 * self.get_height() / max(content.get_height(), content.get_width())
        content.scale(a)
        bubble_width, bubble_height = self._bubble_dimensions(content)

        ellipse = Ellipse(color=WHITE)
        ellipse.stretch_to_fit_height(bubble_height)
        ellipse.stretch_to_fit_width(bubble_width)
        ellipse.surround(content).scale(1.2)

        bubble1 = Circle(color=WHITE).set(width=self.get_width() / 5)
        bubble2 = Circle(color=WHITE).set(width=self.get_width() / 2)
        mob_start = self.get_corner(UR) + self.get_height() / 10 * UP
        bubble1.move_to(mob_start)
        bubble2.next_to(bubble1, UR, buff=0.03)
        ellipse.next_to(bubble2, UR, buff=0.03)
        content.scale(0.7)
        content.move_to(ellipse)

        return VGroup(ellipse, bubble1, bubble2).set_stroke(width=1)

    def left_thought_bubble(self, content) -> VGroup:
        a = 1.5 * self.get_height() / max(content.get_height(), content.get_width())
        content.scale(a)

        if content.get_width() > content.get_height():
            bubble_width = content.get_width()
            bubble_height = max(content.get_width() / 2, content.get_height())
        else:
            bubble_height = content.get_height()
            bubble_width = max(content.get_height() / 2, content.get_width())

        ellipse = Ellipse(color=WHITE)
        ellipse.stretch_to_fit_height(bubble_height)
        ellipse.stretch_to_fit_width(bubble_width)
        ellipse.surround(content)

        bubble1 = Circle(color=WHITE).set(width=self.get_width() / 5)
        bubble2 = Circle(color=WHITE).set(width=self.get_width() / 2)
        mob_start = self.get_center() + UL * 0.6 * self._tail_start_factor()
        bubble1.move_to(mob_start)
        bubble2.next_to(bubble1, UL, buff=-0.05)
        ellipse.next_to(bubble2, UL, buff=-0.05)
        content.scale(0.8)
        content.move_to(ellipse)

        return VGroup(ellipse, bubble1, bubble2).set_stroke(width=1)


# Legacy alias
Euler_Creature = EulerCreature
