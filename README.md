# Manim Videos (Paramat)

Repo d'organisation des projets **Manim Community Edition** pour les vidéos YouTube.

## Setup (macOS)

```bash
cd "/Users/nicolasmasset/Desktop/ROOT/taff/Projets/Youtube/Manim Videos"
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/pip install manim
.venv/bin/pip install -e .
```

Vérifier `ffmpeg` (requis pour encoder les vidéos) :

```bash
ffmpeg -version
```

## Rendre une scène

Exemple (qualité low pour tests) :

```bash
.venv/bin/manim -pql videos/complexes/scenes.py SquareToCircle
```

## Démo créature (EulerCreature)

```bash
.venv/bin/manim -pql videos/complexes/scenes.py EulerCreatureDemo
```

Notes:
- La démo de créature **n’utilise pas LaTeX**.
- Pour `MathTex/Tex` dans tes vraies vidéos, installe LaTeX (ex: MacTeX/BasicTeX).
