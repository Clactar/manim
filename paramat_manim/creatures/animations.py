from __future__ import annotations

from manim import ApplyMethod, there_and_back, squish_rate_func


class Blink(ApplyMethod):
    def __init__(self, creature, **kwargs):
        kwargs.setdefault("rate_func", squish_rate_func(there_and_back))
        super().__init__(creature.blink, **kwargs)


class Look_Direction(ApplyMethod):
    def __init__(self, creature, vect, **kwargs):
        super().__init__(creature.look_in_direction, vect, **kwargs)


class Look_Mobject(ApplyMethod):
    def __init__(self, creature, mob, **kwargs):
        super().__init__(creature.look_at, mob, **kwargs)


class Reset_Look(ApplyMethod):
    def __init__(self, creature, **kwargs):
        super().__init__(creature.look_reset, **kwargs)


class Angry(ApplyMethod):
    def __init__(self, creature, **kwargs):
        super().__init__(creature.angry, **kwargs)


class Think(ApplyMethod):
    def __init__(self, creature, **kwargs):
        super().__init__(creature.thinking, **kwargs)


class Happy(ApplyMethod):
    def __init__(self, creature, **kwargs):
        super().__init__(creature.happy, **kwargs)


class Happy_Reset(ApplyMethod):
    def __init__(self, creature, **kwargs):
        super().__init__(creature.happy_reset, **kwargs)


