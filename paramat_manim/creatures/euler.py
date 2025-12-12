from __future__ import annotations

from dataclasses import dataclass, field
import shutil
from typing import Optional

import numpy as np
from manim import (
    BLACK,
    BLUE,
    RIGHT,
    UL,
    UP,
    UR,
    Arc,
    Circle,
    Dot,
    Ellipse,
    Line,
    MathTex,
    Text,
    VGroup,
    normalize,
)


@dataclass(frozen=True)
class EulerCreatureStyle:
    body_color: str = BLUE
    body_scale: float = 8.2
    body_font: str = "Helvetica"
    use_tex: Optional[bool] = None  # None => auto (uses TeX only if `latex` is available)
    pupil_color: str = BLACK
    eye_scale: float = 1.5
    pupil_scale: float = 0.75
    glint_scale: float = 0.2
    eye_spacing: float = 0.001
    eye_up_buff: float = -0.02
    mouth_shift: np.ndarray = field(default_factory=lambda: np.array([-0.9, 0.5, 0.0]))
    mouth_scale: float = 1.0


class EulerCreature(VGroup):
    """
    Simple 'e' creature (eyes + mouth) inspired by the older codebase.

    Public API kept close to your legacy scripts:
    - eyes: blink/look_in_direction/look_at/look_reset
    - expressions: happy/happy_reset/angry/thinking
    - bubbles: right_speech_bubble/left_speech_bubble/right_thought_bubble/left_thought_bubble
    """

    def __init__(self, color: str = BLUE, style: Optional[EulerCreatureStyle] = None, **kwargs):
        super().__init__(**kwargs)
        self.style = style or EulerCreatureStyle(body_color=color)

        # Body
        use_tex = self.style.use_tex
        if use_tex is None:
            use_tex = shutil.which("latex") is not None

        if use_tex:
            self.body = MathTex("e", color=self.style.body_color).scale(self.style.body_scale)
        else:
            self.body = Text("e", color=self.style.body_color, font=self.style.body_font).scale(self.style.body_scale)

        # Eyes (sclera)
        self.left_eye = Dot(color="WHITE").scale(self.style.eye_scale).next_to(
            self.body, UP, buff=self.style.eye_up_buff
        )
        self.right_eye = Dot(color="WHITE").scale(self.style.eye_scale).next_to(
            self.left_eye, RIGHT, buff=-self.style.eye_spacing
        )

        # Pupils (black + glint)
        self.left_pupil = Dot(color=self.style.pupil_color).scale(self.style.pupil_scale).move_to(self.left_eye)
        self.left_glint = Dot(color="WHITE").scale(self.style.glint_scale).next_to(
            self.left_pupil, UR, buff=-0.05
        )
        self.right_pupil = Dot(color=self.style.pupil_color).scale(self.style.pupil_scale).move_to(self.right_eye)
        self.right_glint = Dot(color="WHITE").scale(self.style.glint_scale).next_to(
            self.right_pupil, UR, buff=-0.05
        )

        # Mouth (default: happy)
        self.mouth = Text("(").rotate(np.pi / 2).next_to(self.body, buff=0).shift(self.style.mouth_shift)
        if self.style.mouth_scale != 1.0:
            self.mouth.scale(self.style.mouth_scale)

        self.add(
            self.body,
            self.left_eye,
            self.right_eye,
            self.left_pupil,
            self.left_glint,
            self.right_pupil,
            self.right_glint,
            self.mouth,
        )

    # -------------------------------------------------------------------------
    # Parts helpers
    # -------------------------------------------------------------------------

    def get_body(self) -> MathTex:
        return self.body

    def get_eyes(self) -> VGroup:
        return VGroup(
            self.left_eye,
            self.right_eye,
            self.left_pupil,
            self.left_glint,
            self.right_pupil,
            self.right_glint,
        )

    def get_pupils(self) -> VGroup:
        return VGroup(self.left_pupil, self.left_glint, self.right_pupil, self.right_glint)

    # -------------------------------------------------------------------------
    # Eye animations / pose helpers
    # -------------------------------------------------------------------------

    def blink(self, **_kwargs) -> "EulerCreature":
        """
        Collapse all eye parts to the bottom y of the eyes group.
        Intended to be used via ApplyMethod/there_and_back.
        """
        eyes = self.get_eyes()
        bottom_y = eyes.get_bottom()[1]
        for submob in eyes:
            submob.apply_function(lambda p: np.array([p[0], bottom_y, p[2]]))
        return self

    def _max_pupil_offset(self) -> float:
        # Approximate: sclera radius - pupil radius.
        sclera_r = self.left_eye.get_width() / 2
        pupil_r = self.left_pupil.get_width() / 2
        return max(0.0, sclera_r - pupil_r - 0.02 * sclera_r)

    def look_in_direction(self, target: np.ndarray) -> "EulerCreature":
        """
        Move pupils towards a target point, clamped so they remain inside the sclera.
        """
        max_offset = self._max_pupil_offset()
        eyes_center = VGroup(self.left_eye, self.right_eye).get_center()
        direction = normalize(target - eyes_center)
        offset = direction * max_offset

        self.left_pupil.move_to(self.left_eye.get_center() + offset)
        self.left_glint.next_to(self.left_pupil, UR, buff=-0.05)
        self.right_pupil.move_to(self.right_eye.get_center() + offset)
        self.right_glint.next_to(self.right_pupil, UR, buff=-0.05)
        return self

    def look_at(self, mob) -> "EulerCreature":
        return self.look_in_direction(mob.get_center())

    def look_reset(self) -> "EulerCreature":
        self.left_pupil.move_to(self.left_eye)
        self.left_glint.next_to(self.left_pupil, UR, buff=-0.05)
        self.right_pupil.move_to(self.right_eye)
        self.right_glint.next_to(self.right_pupil, UR, buff=-0.05)
        return self

    # -------------------------------------------------------------------------
    # Expressions
    # -------------------------------------------------------------------------

    def happy(self) -> "EulerCreature":
        new_mouth = Text("(").rotate(np.pi / 2).move_to(self.mouth)
        new_mouth.set(width=self.mouth.get_width())
        self.mouth.become(new_mouth)
        return self

    def happy_reset(self) -> "EulerCreature":
        return self.happy().look_reset()

    def angry(self) -> "EulerCreature":
        # Simple angry mouth + slightly squashed eyes (visual cue)
        new_mouth = Text("(").rotate(-np.pi / 2).move_to(self.mouth)
        new_mouth.set(width=self.mouth.get_width())
        self.mouth.become(new_mouth)
        self.left_eye.stretch_to_fit_height(self.left_eye.get_height() * 0.9)
        self.right_eye.stretch_to_fit_height(self.right_eye.get_height() * 0.9)
        return self

    def thinking(self) -> "EulerCreature":
        new_mouth = Text("/").rotate(-np.pi / 3).move_to(self.mouth)
        new_mouth.set(width=self.mouth.get_width())
        self.mouth.become(new_mouth)
        self.left_eye.stretch_to_fit_width(self.left_eye.get_width() * 1.1)
        self.right_eye.stretch_to_fit_width(self.right_eye.get_width() * 1.1)
        return self

    # -------------------------------------------------------------------------
    # Bubbles
    # -------------------------------------------------------------------------

    def _scale_bubble_content(self, content) -> None:
        a = 1.5 * self.get_height() / max(content.get_height(), content.get_width())
        content.scale(a)

    def right_speech_bubble(self, content):
        self._scale_bubble_content(content)
        content.next_to(self, UR, buff=0.5)

        ellipse = Arc(start_angle=-4 * np.pi / 6, angle=15 * np.pi / 8)
        ellipse.stretch_to_fit_height(1.2 * max(content.get_height(), content.get_width() / 2))
        ellipse.stretch_to_fit_width(1.2 * max(content.get_width(), content.get_height() / 2))
        ellipse.move_to(content).scale(1.2)

        tail_start = self.get_center() + UR * 0.6
        left_line = Line(tail_start, ellipse.get_start())
        right_line = Line(tail_start, ellipse.get_end())
        outline = VGroup(ellipse, left_line, right_line).set_stroke(width=1)
        return VGroup(outline, content)

    def left_speech_bubble(self, content):
        self._scale_bubble_content(content)
        content.next_to(self, UL, buff=0.5)

        ellipse = Arc(start_angle=-np.pi / 6, angle=15 * np.pi / 8)
        ellipse.stretch_to_fit_height(1.2 * max(content.get_height(), content.get_width() / 2))
        ellipse.stretch_to_fit_width(1.2 * max(content.get_width(), content.get_height() / 2))
        ellipse.move_to(content).scale(1.2)

        tail_start = self.get_center() + UL * 0.6
        left_line = Line(tail_start, ellipse.get_start())
        right_line = Line(tail_start, ellipse.get_end())
        outline = VGroup(ellipse, left_line, right_line).set_stroke(width=1)
        return VGroup(outline, content)

    def right_thought_bubble(self, content):
        self._scale_bubble_content(content)
        ellipse = Ellipse(color="WHITE").surround(content).scale(1.2)
        bubble1 = Circle(color="WHITE").set(width=self.get_width() / 5)
        bubble2 = Circle(color="WHITE").set(width=self.get_width() / 2)

        start = self.get_corner(UR) + self.get_height() / 10 * UP
        bubble1.move_to(start)
        bubble2.next_to(bubble1, UR, buff=0.03)
        ellipse.next_to(bubble2, UR, buff=0.03)
        content.scale(0.7).move_to(ellipse)
        return VGroup(VGroup(ellipse, bubble1, bubble2).set_stroke(width=1), content)

    def left_thought_bubble(self, content):
        self._scale_bubble_content(content)
        ellipse = Ellipse(color="WHITE").surround(content).scale(1.2)
        bubble1 = Circle(color="WHITE").set(width=self.get_width() / 5)
        bubble2 = Circle(color="WHITE").set(width=self.get_width() / 2)

        start = self.get_corner(UL) + self.get_height() / 10 * UP
        bubble1.move_to(start)
        bubble2.next_to(bubble1, UL, buff=0.03)
        ellipse.next_to(bubble2, UL, buff=0.03)
        content.scale(0.7).move_to(ellipse)
        return VGroup(VGroup(ellipse, bubble1, bubble2).set_stroke(width=1), content)


# Backwards-compatible alias (legacy name)
Euler_Creature = EulerCreature


