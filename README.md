# Manim Videos (Paramat)

Repo pour les vidéos **Manim Community Edition** de la chaîne YouTube Paramat.

## Setup (macOS)

```bash
cd "/Users/nicolasmasset/Desktop/ROOT/taff/Projets/Youtube/Manim Videos"
python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install manim
.venv/bin/pip install -e .
```

### LaTeX (requis pour le beau "e" italique)

```bash
brew install --cask basictex
# Puis redémarrer le terminal
```

Sans LaTeX, le fallback utilise Times New Roman italic (moins joli).

### FFmpeg (requis pour encoder les vidéos)

```bash
brew install ffmpeg
```

## Rendre une scène

```bash
.venv/bin/manim -pql videos/complexes/scenes.py SquareToCircle
```

## Démo créature (EulerCreature)

```bash
.venv/bin/manim -pql videos/complexes/scenes.py EulerCreatureDemo
```

## Structure

```
paramat_manim/          # Module réutilisable (créature, helpers)
  creatures/
    euler.py            # EulerCreature (le "e" animé)
    animations.py       # Blink, Look_Mobject, etc.
videos/
  complexes/            # Projet vidéo "Les Nombres Complexes"
    scenes.py
    assets/
    audio/
```
