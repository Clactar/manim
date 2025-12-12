from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

import numpy as np
from manim import (
    BLUE,
    UL,
    UP,
    UR,
    Arc,
    Circle,
    Ellipse,
    Line,
    SVGMobject,
    VGroup,
    normalize,
)


@dataclass(frozen=True)
class EulerCreatureStyle:
    """
    Style options for EulerCreature.

    Default is to use the bundled SVG assets (matches your old repo output).
    """

    color: str = BLUE  # currently unused when using SVG (SVG has baked colors)
    scale: float = 1.0
    use_svg: Optional[bool] = None  # None => auto (use SVG if assets exist)


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
        self.style = style or EulerCreatureStyle(color=color)

        assets_dir = Path(__file__).resolve().parents[1] / "assets" / "creatures" / "e"
        happy_svg = assets_dir / "shappy.svg"
        think_svg = assets_dir / "squest.svg"
        angry_svg = assets_dir / "sangry.svg"

        use_svg = self.style.use_svg
        if use_svg is None:
            use_svg = happy_svg.exists()

        if not use_svg:
            raise RuntimeError(
                "EulerCreature expects SVG assets. Missing "
                f"`{happy_svg}`. Reinstall or ensure assets are present."
            )

        base = SVGMobject(str(happy_svg))

        # Layout matches your old `studeo_creature.py` slicing:
        # body: [0:4], left_white: [4], left_pupil: [5:7],
        # right_white: [7], right_pupil: [8:10], mouth: [10]
        self.body = base[0:4].copy()
        self.left_white = base[4].copy()
        self.left_pupil = base[5:7].copy()
        self.right_white = base[7].copy()
        self.right_pupil = base[8:10].copy()
        self.mouth = base[10].copy()

        self.add(self.body, self.left_white, self.right_white, self.left_pupil, self.right_pupil, self.mouth)

        if self.style.scale != 1.0:
            self.scale(self.style.scale)

        # Cache mouth templates for expressions (scaled/moved at swap time)
        self._mouth_templates = {
            "happy": SVGMobject(str(happy_svg))[10],
            "thinking": SVGMobject(str(think_svg))[10],
            "angry": SVGMobject(str(angry_svg))[10],
        }

    # -------------------------------------------------------------------------
    # Parts helpers
    # -------------------------------------------------------------------------

    def get_body(self):
        return self.body

    def get_eyes(self) -> VGroup:
        return VGroup(self.left_white, self.right_white, self.left_pupil, self.right_pupil)

    def get_pupils(self) -> VGroup:
        return VGroup(self.left_pupil, self.right_pupil)

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

    def look_in_direction(self, target: np.ndarray) -> "EulerCreature":
        """
        Move pupils towards a target point, clamped so they remain inside the sclera.
        """
        coeff = min(
            self.left_white.get_width(),
            self.left_white.get_height(),
            self.left_pupil.get_width(),
            self.left_pupil.get_height(),
        ) / 2
        eyes_center = VGroup(self.left_white, self.right_white, self.left_pupil, self.right_pupil).get_center()
        direction = normalize(target - eyes_center) * coeff

        left_center = self.left_white.get_center()
        right_center = self.right_white.get_center()
        self.left_pupil.move_to(left_center + direction)
        self.right_pupil.move_to(right_center + direction)
        return self

    def look_at(self, mob) -> "EulerCreature":
        return self.look_in_direction(mob.get_center())

    def look_reset(self) -> "EulerCreature":
        self.left_pupil.move_to(self.left_white.get_center())
        self.right_pupil.move_to(self.right_white.get_center())
        return self

    # -------------------------------------------------------------------------
    # Expressions
    # -------------------------------------------------------------------------

    def _swap_mouth(self, key: str) -> None:
        tmpl = self._mouth_templates[key].copy()
        tmpl.set(width=self.mouth.get_width())
        tmpl.move_to(self.mouth)
        self.mouth.become(tmpl)

    def happy(self) -> "EulerCreature":
        self._swap_mouth("happy")
        return self

    def happy_reset(self) -> "EulerCreature":
        return self.happy().look_reset()

    def angry(self) -> "EulerCreature":
        self._swap_mouth("angry")
        return self

    def thinking(self) -> "EulerCreature":
        self._swap_mouth("thinking")
        return self

    # -------------------------------------------------------------------------
    # Bubbles
    # -------------------------------------------------------------------------

    def _scale_bubble_content(self, content) -> None:
        a = 2.0 * self.get_height() / max(content.get_height(), content.get_width())
        content.scale(a)

    def right_speech_bubble(self, content):
        self._scale_bubble_content(content)
        content.next_to(self, UR, buff=0.5)

        ellipse = Arc(start_angle=-4 * np.pi / 6, angle=15 * np.pi / 8)
        ellipse.stretch_to_fit_height(1.2 * max(content.get_height(), content.get_width() / 2))
        ellipse.stretch_to_fit_width(1.2 * max(content.get_width(), content.get_height() / 2))
        ellipse.move_to(content).scale(1.2)

        tail_start = self.get_corner(UR) + self.get_height() / 10 * UP
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

        tail_start = self.get_corner(UL) + self.get_height() / 10 * UP
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


